# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:34:16 2019

@author: yqlim
"""
import logging

logger = logging.getLogger(__name__)

import win32com.client
import re
import pytz
from bs4 import BeautifulSoup as bs

from .fso import file_exists

def send_email(str_to, 
               str_cc, 
               str_bcc, 
               str_subject, 
               str_body, 
               bln_send = False, 
               dte_delay = None, 
               str_mailbox_to_use = None, 
               lst_attachment_paths = None):
    """
    Sends email through Outlook application via win32com.
    
    Parameters
    ----------
    str_to : string
        string containing email addresses of intended recipients separated by ';'
    str_cc : string
        string containing email addresses of cc recipients separated by ';'
    str_bcc : string 
        string containing email addresses of bcc recipients separated by ';'
    str_subject : string 
        string representing email subject
    str_body : string
        email content - if '<HTML>' tag is present, content will be applied to 
        email's `HTMLBody` property instead of email's `Body` property
    bln_send : boolean
        True to automatically send out email (default: False)
    dte_delay : datetime
        (delayed) datetime to send out email
    str_mailbox_to_use : string
        email address of mailbox to use
    lst_attachment_paths : list
        list of full file paths of files to attach to email
    
    Returns
    -------
    boolean
        True if email is successfully sent
    """
    outlook = win32com.client.DispatchEx('Outlook.Application')
    if str_mailbox_to_use:
        namespace = outlook.GetNamespace('MAPI')
        recipient = namespace.CreateRecipient(str_mailbox_to_use)
        recipient.Resolve()
        try:
            folder = namespace.Folders[str_mailbox_to_use].Folders["Inbox"]
        except:
            logger.error('Mailbox not found.')
            return False
        if not folder:
            logger.error('Inbox not found in specified mailbox.')
            return False
        mail_item = folder.Items.Add()
    else:
        mail_item = outlook.CreateItem(0)
    mail_item.To = str_to
    mail_item.CC = str_cc
    mail_item.BCC = str_bcc
    mail_item.Subject = str_subject
    if '<html>' in str_body.lower():
        mail_item.HTMLBody = str_body
    else:
        mail_item.Body = str_body
    if lst_attachment_paths:
        for attachment in lst_attachment_paths:
            if file_exists(attachment):
                mail_item.Attachments.Add(attachment)
            else:
                logger.info(str(attachment) + ' does not exist.')
    if dte_delay:
        mail_item.DeferredDeliveryTime = dte_delay
    if bln_send:
        mail_item.Send()
    else:
        mail_item.Display()
    return True

def reply(email, 
          str_body,
          str_to='',
          str_cc='',
          str_bcc='',
          str_subject='',
          bln_send=False,
          dte_delay=None,          
          lst_attachment_paths=None):
    """
    Reply win32com email.
    
    Parameters
    ----------
    str_body : str
        email content - if '<HTML>' tag is present, content will be applied to
        email's `HTMLBody` property instead of email's `Body` property.
    str_to : str, optional
        string containing email addresses of intended recipients to be included
        above and beyond existing recipients,  separated by ';' (default is '', 
        which implies original intended recipients).
    str_cc : str, optional
        string containing email addresses of cc recipients, separated by ';' 
        (default is '', which implies original cc recipients).
    str_bcc : str, optional
        string containing email addresses of bcc recipients, separated by ';'
        (default value is '', which implies no bcc recipients).
    str_subject : str, optional
        string representing email subject to prepend to original email subject,
        enclosed in square brackets '[]'.
    bln_send : boolean, optional
        determine if email is automatically sent out (default value is False, 
        which displays email instead of sending it).
    dte_delay : datetime, optional
        delayed datetime to send out email (default value is `None`, which implies
        email will be sent immediately).
    lst_attachment_paths : list, optional
        list of full paths of files to attach to email (default value is `None`,
        which implies no file to attach to email).
    
    Returns
    -------
    boolean
        True if email is successfully sent/generated.
    """    
    mail_item = email.Reply()
    mail_item.To = mail_item.To + ';' + str_to
    mail_item.CC = str_cc
    mail_item.BCC = str_bcc
    mail_item.Subject = '[' + str_subject + '] ' + mail_item.Subject
    if '<html>' in str_body.lower():
        mail_item.HTMLBody = str_body + '<br/><br/>' + mail_item.HTMLBody
    else:
        mail_item.Body = str_body + '\n\n' + mail_item.Body
    if lst_attachment_paths:
        for attachment in lst_attachment_paths:
            if file_exists(attachment):
                mail_item.Attachments.Add(attachment)
            else:
                logger.info(str(attachment) + ' does not exist.')
    if dte_delay:
        mail_item.DeferredDeliveryTime = dte_delay
    if bln_send:
        mail_item.Send()
    else:
        mail_item.Display()
    return True

def email_recipient_names_to_addresses(str_email_names, mail_item):
    """
    Convert email recipient names to mail addresses.
    
    Parameters
    ----------
    str_email_names : string
        string containing names of recipients in `mail_item` object
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        mail addresses of recipients in `mail_item` object
    """
    dic_email_addresses = dict()
    str_output = ''
    dic_email_addresses = get_all_recipients_SMTP_mail_addresses(mail_item)
    temp = str_email_names.split('; ')
    for name in temp:
        if name.strip() != '':
            str_output = str_output + str(dic_email_addresses[name]) + '; '        
    return str_output.strip()

def get_sender_SMTP_mail_address(mail_item):
    """
    Returns sender's SMTP mail address.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        SMTP mail address of sender
    """
    reply = mail_item.Reply()
    recipient = reply.Recipients[1]
    str_address = recipient.PropertyAccessor.GetProperty(r'http://schemas.microsoft.com/mapi/proptag/0x39FE001E').strip()                
    return str_address

def get_all_recipients_SMTP_mail_addresses(mail_item):
    """
    Returns dictionary containing SMTP mail addresses of all recipients in 
    `mail_item` object.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    dictionary
        contains {recipient_name : SMTP_mail_address} key-value pairs of all 
        recipients in `mail_item` object
    """
    dic_outputs = dict()
    for recipient in mail_item.Recipients:
        dic_outputs[recipient.Name] = recipient.PropertyAccessor.GetProperty(r'http://schemas.microsoft.com/mapi/proptag/0x39FE001E').strip()
    return dic_outputs

def get_real_attachment_count(mail_item):
    """
    Count the number of real attachments in the `mail_item` object.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        email address of mailbox
    """
    i = 0
    for attachment in mail_item.Attachments:
        str_cid = attachment.PropertyAccessor.GetProperty(r'http://schemas.microsoft.com/mapi/proptag/0x3712001E')
        if str_cid == '':
            i = i + 1
    return i

def get_mailbox_from_mailitem(mail_item):
    """
    Return mailbox to which `mail_item` belongs to.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    string
        email address of mailbox
    """
    parent = mail_item.Parent
    name = parent.Name
    while not '@' in name:
        parent = parent.Parent
        name = parent.Name
        
    return name

def get_basic_email_details(mail_item, timezone='Asia/Singapore'):
    """
    Returns a dictionary containing basic properties of an Outlook `mail_item` object.
    
    Parameters
    ----------
    mail_item : Outlook Mailitem
        Outlook mailitem object
    
    Returns
    -------
    dictionary
        containing basic properties/attributes of an Outlook `mail_item` object
        {property_name : property_value}
    """
    dic_basic_email_details = dict()
    dic_basic_email_details['Mailbox'] = get_mailbox_from_mailitem(mail_item)
    dic_basic_email_details['EntryID'] = mail_item.EntryID
    dic_basic_email_details['StoreID'] = mail_item.Parent.StoreID
    dic_basic_email_details['To'] = email_recipient_names_to_addresses(mail_item.To, mail_item)
    dic_basic_email_details['From'] = get_sender_SMTP_mail_address(mail_item)
    dic_basic_email_details['Cc'] = email_recipient_names_to_addresses(mail_item.CC, mail_item)
    dic_basic_email_details['Subject'] = mail_item.Subject
    dic_basic_email_details['ConversationID'] = mail_item.ConversationID
    dic_basic_email_details['ConversationIndex'] = mail_item.ConversationIndex                     
    dic_basic_email_details['ConversationTopic'] = mail_item.ConversationTopic
    dic_basic_email_details['Body'] = re.sub(r'\r\n', ' ', mail_item.Body)
    dic_basic_email_details['HTMLBody'] = mail_item.HTMLBody
    dic_basic_email_details['SentOn'] = mail_item.SentOn.astimezone(pytz.timezone(timezone))
    dic_basic_email_details['ReceivedOn'] = mail_item.ReceivedTime.astimezone(pytz.timezone(timezone))
    dic_basic_email_details['Attachment'] = (get_real_attachment_count(mail_item) > 0)
    return dic_basic_email_details

def html_to_tables(str_HTML):
    """Extracts tables from html body of Outlook email"""
    objHTML = bs(str_HTML, 'lxml')
    objTables = objHTML.findAll('table')
    arrTable = []
    for objTable in objTables:
        arrRow = []
        for objRow in objTable.findAll('tr'):
            arrCol = []
            _ = objRow.findAll('th')
            if not _:
                _ = objRow.findAll('td')
            for objCol in _:
                arrCol.append(objCol.get_text().strip())                
            arrRow.append(arrCol)            
        arrTable.append(arrRow)    
    return arrTable

def table_to_html(lst_table,
                  bln_header = True):
    
    str_html = '<table style="width:100%; border-collapse:collapse;", border=1>'
    first_row = 0
    if bln_header:
        str_html = str_html + '<tr>'
        for i in range(len(lst_table[0])):
            str_html = str_html + '<th>' + str(lst_table[0][i]) + '</th>'
        str_html = str_html + '</tr>'
        first_row = 1
    
    for i in range(first_row, len(lst_table)):
        str_html = str_html + '<tr>'
        for j in range(len(lst_table[i])):
            str_html = str_html + '<td>' + str(lst_table[i][j]) + '</td>'
            
        str_html = str_html + '</tr>'
        
    str_html = str_html + '</table>'
    return str_html