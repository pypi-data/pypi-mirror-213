# -*- coding: utf-8 -*-
import win32com.client

class mail:
    def __init__(self):
        self.outlook = win32com.client.dynamic.Dispatch('Outlook.Application')
        self.namespace = self.outlook.GetNamespace("MAPI")

    def get_mail_total_mail_no_by_folder(self, folder_name):
        result = self.namespace.Folders[folder_name].Folders.items.count
        return result

    def read_total_unread_mail_no(self, folder_name):
        input_folder = self.namespace.Folders[folder_name].Folders.items.count
        result = input_folder.UnReadItemsCount
        return result

    def get_one_email_information(self, one_email):
        result = {}
        result["sender"] = one_email.SenderName
        result["receiver"] = one_email.To
        result["title"] = one_email.Subject
        result["time"] = one_email.ReceivedTime
        result["body"] = one_email.Body
        return result

    def get_top_folder_names(self):
        result = []
        for no in range(self.namespace.Folders.count):
            this_name = self.namespace.Folders[no].Name
            result.append([no, this_name])
        return result

    def get_sub_folders_names(self, folder_name):
        result = []
        for no in range(self.namespace.Folders[folder_name].Folders.count):
            this_name = self.namespace.Folders[folder_name].Folders[no].name
            result.append([folder_name, no, this_name])
        return result


    def read_basic_input_mails_data(self):
        input_folder = self.namespace.GetDefaultFolder(6)
        for message in input_folder.Items:
            print(message.Subject)

    def read_unread_mail_from_basic_input_folder(self):
        input_folder = self.namespace.GetDefaultFolder(6)
        for message in input_folder.Items.Restrict("Unread]=true"):
            print(message.Subject)

    def get_latest_mail_items_in_input_mail_box(self, input_no = 5):
        result = []
        input_folder = self.namespace.GetDefaultFolder(6)
        messages = input_folder.Items
        messages.Sort("ReceivedTime",True)
        message = messages.GetFirst()

        for no in range(input_no):
            print(message.Subject)
            message = messages.GetNext()
            result.append(message)
        return result

    def get_mail_items_in_folder(self, folder_object, input_no=5):
        result = []
        messages = folder_object.Items
        messages.Sort("ReceivesTime", True)
        message = messages.GetFirst()

        for no in range(input_no):
            print(message.Subject)
            message = messages.GetNext()
            result.append(message)
        return result

    def get_10_latest_in_mail(self):
        result = []
        many_mail = self.get_latest_mail_items_in_input_mail_box(10)
        for num in range(len(many_mail)):
            temp = self.get_one_email_information(many_mail[num])
            result.append(temp)
        return result

    def get_basic_promise_folder(self):
        input_folder = self.namespace.GetDefaultFolder(9)
        return input_folder

    def get_basic_draft_folder(self):
        input_folder = self.namespace.GetDefaultFolder(16)
        return input_folder

    def get_basic_input_folder(self):
        input_folder = self.namespace.GetDefaultFolder(6)
        return input_folder

    def send_mail(self, input_dic):
        new_mail = self.outlook.CreateItem(0)
        new_mail.To = input_dic["to"]
        new_mail.Subject = input_dic["subject"]
        new_mail.Body = input_dic["body"]
        #attachment = "첨부화일들"
        #new_mail.Attachments.Add(attachment)
        new_mail.Send()


    def check_outlook_email_test(self, ):
        """
        아웃룩익스프레스 테스트 하는것
        """
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")

        input_folder = namespace.GetDefaultFolder(6)
        # print("폴더이름 ==> ", input_folder.Name)

        for i in input_folder.items:
            print(i.subject)
            print(str(i.Sender) + "\t: " + i.SenderEmailAddress)

        print("전체 메일 개수 :" + str(input_folder.items.count))
        print("읽지않은 메일 개수 :" + str(input_folder.UnReadItemCount))
        print("읽은 메일 개수 :" + str(input_folder.items.count - input_folder.UnReadItemCount))

        print(namespace.Folders[0].Name)
        print(namespace.Folders[1].Name)
        print(namespace.Folders[2].Name)

        root_folder = namespace.Folders.Item(1)
        for folder in root_folder.Folders:
            print("폴더이름 ==> ", folder.Name)
            print("갯수 ==> ", folder.items.count)

        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        root_folder = namespace.Folders.Item(1)
        subfolder = root_folder.Folders['All'].Folders['Main Folder'].Folders['Subfolder']
        messages = subfolder.Items

aa = mail()
folder = aa.get_10_latest_in_mail()
for one in folder:
    print(one)