"""
Dynamo Gas is native app for transaction entry, analysis, and visualization
"""
from asyncio import subprocess
from platform import platform
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT, Pack
from datetime import datetime
import pandas as pd
import os
import platform
from tabulate import tabulate
import subprocess

# print(pd.__version__)

now = datetime.now()
# dd/mm/YY H:M:S
date_time = now.strftime("%B %d, %Y")
date_and_time = now.strftime("%B %d, %Y | %H:%M:%S")


class DynamoGas(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        label_font_size = 10
        label_font_color = '#fff'  # '#ffe5b4'
        button_1_color = '#0aa1dd'  # '#B1E1FF' '#ffe5b4'
        print_apply_button_color = '#2155cd'  # '#eb5353'
        button_1_font_size = 9
        font_family = 'system'
        if platform.system() == 'Windows':
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')
            self.database_path = str(desktop_path)+'\DataBase.csv'
        if platform.system()=='Darwin':
            desktop_path = os.path.expanduser("~/Desktop")
            self.database_path = str(desktop_path)+'/DataBase.csv'

        # Create Name output box
        name_box = toga.Box(style=Pack(direction=COLUMN))
        self.name_input = toga.TextInput(
            placeholder="Enter name of Customer", style=Pack(flex=1, padding_left=5))

        name_label = toga.Label(
            'Name of Customer', style=Pack(text_align=LEFT, width=500, padding_left=5, font_family=font_family, font_size=label_font_size, color=label_font_color))
        name_box.add(name_label)
        name_box.add(self.name_input)

        # Create Phone output box
        phone_box = toga.Box(style=Pack(direction=COLUMN, padding_top=5))
        self.phone_input = toga.TextInput(placeholder="Enter Phone number",
                                          style=Pack(flex=1, padding_left=5))
        phone_label = toga.Label('Phone No.', style=Pack(
            text_align=LEFT, width=500, padding_left=5, font_family=font_family, font_size=label_font_size, color=label_font_color))
        phone_box.add(phone_label)
        phone_box.add(self.phone_input)

        # Create Price per kg box
        price_perkg_box = toga.Box(style=Pack(direction=COLUMN, padding_top=5))
        self.price_perkg_input = toga.TextInput(initial=0,
            style=Pack(flex=1, padding_left=5))
        price_perkg_label = toga.Label('Price per kg.', style=Pack(
            text_align=LEFT, width=500, padding_left=5, font_family=font_family, font_size=label_font_size, color=label_font_color))
        price_perkg_box.add(price_perkg_label)
        price_perkg_box.add(self.price_perkg_input)
        self.price_perkg = self.price_perkg_input.value

        # Create Amount Paid box
        amount_paid_box = toga.Box(style=Pack(direction=COLUMN, padding_top=5))
        self.amount_paid_input = toga.TextInput(initial=0,
            style=Pack(flex=1, padding_left=5))
        amount_paid_label = toga.Label('Amount paid', style=Pack(
            text_align=LEFT, width=500, padding_left=5, font_family=font_family, font_size=label_font_size, color=label_font_color))
        amount_paid_box.add(amount_paid_label)
        amount_paid_box.add(self.amount_paid_input)

        group1_box = toga.Box(
            children=[name_box, phone_box, price_perkg_box, amount_paid_box], style=Pack(direction=COLUMN, padding=0))

        # Create Number of kg box
        number_kg_box = toga.Box(style=Pack(direction=COLUMN))
        self.number_kg_input = toga.TextInput(initial=0,
            style=Pack(flex=1, padding_left=5))
        number_kg_label = toga.Label('Number of Kg', style=Pack(
            text_align=LEFT, width=500, padding_left=5, font_family=font_family, font_size=label_font_size, color=label_font_color))
        number_kg_box.add(number_kg_label)
        number_kg_box.add(self.number_kg_input)

        # Create Purchase Price box
        purchase_price_box = toga.Box(
            style=Pack(direction=COLUMN, padding_top=5))
        self.purchase_price_input = toga.TextInput(initial=0,
            style=Pack(flex=1, padding_left=5))
        purchase_price_label = toga.Label('Purchase Price', style=Pack(
            text_align=LEFT, width=500, padding_left=5, font_family=font_family, font_size=label_font_size, color=label_font_color))
        purchase_price_box.add(purchase_price_label)
        purchase_price_box.add(self.purchase_price_input)

        # Create Debt_Credit box
        debt_credit_box = toga.Box(style=Pack(direction=COLUMN, padding_top=5))
        # Create Debt box
        debt_box = toga.Box(style=Pack(
            direction=COLUMN, padding_left=5))
        self.debt_input = toga.NumberInput(default=0,
            style=Pack(flex=1, padding_left=0))
        debt_label = toga.Label('Debt:', style=Pack(
            text_align=LEFT, width=100, padding_left=0, font_family=font_family, font_size=label_font_size, color=label_font_color))
        debt_box.add(debt_label)
        debt_box.add(self.debt_input)

        # Create Credit box
        credit_box = toga.Box(style=Pack(
            direction=COLUMN, padding_top=5, padding_left=5))
        self.credit_input = toga.NumberInput(default=0,
            style=Pack(flex=1, padding_left=0))
        credit_label = toga.Label('Credit:', style=Pack(
            text_align=LEFT, width=100, padding_left=0, font_family=font_family, font_size=label_font_size, color=label_font_color))
        credit_box.add(credit_label)
        credit_box.add(self.credit_input)
        # Add to debt_credit box
        debt_credit_box.add(debt_box)
        debt_credit_box.add(credit_box)

        group2_box = toga.Box(
            children=[number_kg_box, purchase_price_box, debt_credit_box], style=Pack(direction=COLUMN, padding=0))

        # split = toga.SplitContainer(direction=False, style=Pack(padding=0))
        # split.content = [group1_box, group2_box]

        # Calcuated
        # Create balance box
        balance_box = toga.Box(style=Pack(
            direction=ROW, padding_left=0))
        balance_button = toga.Button(
            'Balance', on_press=self.Balance, style=Pack(width=105, text_align=LEFT, padding_left=0, background_color=button_1_color, color='#fff', font_size=button_1_font_size, font_family=font_family))
        self.calc_balance = toga.TextInput(readonly=True, style=Pack(
            text_align=RIGHT, padding_left=10, padding_top=3))
        balance_box.add(balance_button)
        balance_box.add(self.calc_balance)

        # Create calculated kg box
        kg_calc_box = toga.Box(style=Pack(
            direction=ROW, padding_left=0, padding_top=3))
        kg_calc_button = toga.Button('Calculate Kg', on_press=self.NumberOfKg, style=Pack(width=105, text_align=LEFT, padding_left=0, background_color=button_1_color, color='#fff', font_size=button_1_font_size, font_family=font_family))
        self.calc_kg_calc = toga.TextInput(readonly=True, style=Pack(
            text_align=RIGHT, padding_left=10, padding_top=3))
        kg_calc_box.add(kg_calc_button)
        kg_calc_box.add(self.calc_kg_calc)

        # Create calculated Purchase price box
        price_calc_box = toga.Box(style=Pack(
            direction=ROW, padding_left=0, padding_top=3, padding_bottom=10))
        price_calc_button = toga.Button('Calculate price', on_press=self.PurchasePrice, style=Pack(width=105, text_align=LEFT, padding_left=0, background_color=button_1_color, color='#fff', font_size=button_1_font_size, font_family=font_family))
        self.calc_price_calc = toga.TextInput(readonly=True, style=Pack(
            text_align=RIGHT, padding_left=10, padding_top=3))
        price_calc_box.add(price_calc_button)
        price_calc_box.add(self.calc_price_calc)

        # Create calculate_box
        calculate_box = toga.Box(style=Pack(direction=COLUMN, padding_top=10))
        calculate_box.add(balance_box)
        calculate_box.add(kg_calc_box)
        calculate_box.add(price_calc_box)

        # Create a divider
        horizontal_divider = toga.Divider(direction=0)

        # Create Cleared and not cleared box
        cleared_box = toga.Box(style=Pack(
            direction=ROW, padding_left=0))
        self.cleared = toga.Selection(
            items=['Cleared', 'Not Cleared'], style=Pack(flex=1, padding_left=0))
        self.payment_method = toga.Selection(
            items=['Cash', 'POS', 'Bank transfer'], style=Pack(flex=1, padding_left=5))
        cleared_box.add(self.cleared)
        cleared_box.add(self.payment_method)

        # Create an apply and print button
        apply_button = toga.Button('Apply', on_press=self.append_df_to_excel, style=Pack(
            flex=1, padding_left=100, padding_right=100, background_color=print_apply_button_color, color='#fff', font_family=font_family, font_size=14))
        print_button = toga.Button('Print', on_press=self.printWindow, style=Pack(
            flex=1, padding_left=100, padding_right=100, padding_top=10, background_color=print_apply_button_color, color='#fff', font_family=font_family, font_size=14))

        apply_print_box = toga.Box(children=[apply_button, print_button], style=Pack(
            direction=COLUMN, height=100, padding_top=20))

        self.printer_box = toga.Box(style=Pack(direction=COLUMN))
        self.ok_print = toga.Button('OK',on_press=self.print_slip, style=Pack(padding_left=100, width=100))

        transaction_entry_box = toga.Box(style=Pack(
            direction=COLUMN, padding_left=20, padding_right=20))

        transaction_entry_box.add(group1_box, group2_box)
        transaction_entry_box.add(horizontal_divider)
        transaction_entry_box.add(calculate_box)
        # transaction_entry_box.add(horizontal_divider)
        transaction_entry_box.add(cleared_box)
        transaction_entry_box.add(apply_print_box)

        self.transaction_entry_container = toga.Box(style=Pack(direction=COLUMN))
        self.transaction_entry_container.add(transaction_entry_box)

        # Create Analysis Widgets
        date_box = toga.Box(style=Pack(direction=ROW, padding=10, padding_right=50))
        instruction_label = toga.MultilineTextInput(initial='Follow this date format to analyse your data by date. Example, Year format: 2021, Month format: August 2021 or 2021-08, Day format: August 10, 2021 or 2021-08-10',
                                                    readonly=True, style=Pack(height=70, padding=5, background_color='#c4ddff'))
        date_label = toga.Label('Enter Date:', style=Pack(
            padding_top=5, font_family=font_family))
        self.date_input = toga.TextInput(
            placeholder='Enter date here', style=Pack(flex=1, font_size=13,height=35))
        ok_button = toga.Button('OK', on_press=self.Analysis, style=Pack(
            padding_top=7,padding_left=15, width=40, background_color='#001d6e'))
        # date_box.add(instruction_label)
        date_box.add(date_label)
        date_box.add(self.date_input)
        date_box.add(ok_button)
        date_inst_box = toga.Box(style=Pack(direction=COLUMN))
        date_inst_box.add(instruction_label, date_box)

        # Create Search Database Widgets
        searchby_box = toga.Box(style=Pack(
            direction=ROW, padding=5, padding_right=50))
        searchby_label = toga.Label('Search by:')
        self.searchby_opt = toga.Selection(
            items=['Name of Customer', 'Date', 'Phone Number', 'Status'], style=Pack(flex=1, color='#000'))
        searchby_box.add(searchby_label, self.searchby_opt)

        search_box = toga.Box(style=Pack(
            direction=ROW, padding=5, padding_right=50))
        # search_label = toga.Label('Search:')
        self.search_input = toga.TextInput(placeholder='Search database', style=Pack(
            flex=1,height=35, font_size=12))
        ok_search = toga.Button('OK', on_press=self.Searchresult, style=Pack(
            padding_top=7,padding_left=15, width=40, background_color='#001d6e'))
        search_box.add(self.search_input, ok_search)

        delete_search_table_button = toga.Button('delete tables',
            on_press=self.delete_search_analysis_table, style=Pack(font_family='system', width=130, font_size=10,padding_left=20))

        self.tran_cont_box = toga.Box(style=Pack(
            direction=COLUMN))

        self.trans_analyis_box = toga.Box(style=Pack(
            direction=COLUMN, padding_left=10, padding_right=10))
        self.tran_cont_box.add(date_inst_box, searchby_box, search_box, delete_search_table_button, self.trans_analyis_box)
        
        # self.trans_analyis_box.add()
        self.analyse_table = None
        self.search_table = None
        self.entry_box = None
        self.printers_opt=None
        # Create Commands
        tools = toga.Group('Tools')
        add_user_icon = 'resources/add_male_user_100px.png'
        analysis_icon = 'resources/analysis.png'
        entry_command = toga.Command(self.EntryWindow, tooltip="Enter customer's transaction details",label='Transaction Entry',icon=add_user_icon, group=tools)

        analysis_command = toga.Command(self.AnalysisWindow, tooltip="Analyse data by date ",label='Transaction Analysis',icon=analysis_icon, group=tools)

        entry_button = toga.Button('Enter transaction details', on_press=self.EntryWindow, style=Pack(padding_left=50, padding_right=50,padding_top=50, padding_bottom=30, height=50, background_color='#4b7be5', color='#fff', font_family=font_family, font_size=16))

        # analysis_button = toga.Button('Analyse data by date',
        #                               on_press=self.AnalysisWindow, style=Pack(padding=10, height=100, background_color='#36ae7c', color='#fff', font_family=font_family, font_size=16))

        self.commands.add(entry_command, analysis_command)
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_box.add(entry_button, self.tran_cont_box)

        self.main_box_container = toga.Box(style=Pack(direction=COLUMN))

        self.main_box_container.add(self.main_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box_container
        self.main_window.toolbar.add(entry_command, analysis_command)
        self.main_window.show()

    def NumberOfKg(self, widget, **kwargs):
        Kg = "%8.2f"%(float(self.purchase_price_input.value)/float(self.price_perkg_input.value))
        self.calc_kg_calc.value = str(Kg)

        return self.calc_kg_calc

    def PurchasePrice(self, widget, **kwargs):
        Price = "%8.2f"%(float(self.price_perkg_input.value)*float(self.number_kg_input.value))
        self.calc_price_calc.value = str(Price)
        return self.calc_price_calc

    def Balance(self, widget, **kwargs):
        balances = "%8.2f" % (float(self.amount_paid_input.value)-float(self.purchase_price_input.value))
        self.calc_balance.value = str(balances)
        return self.calc_balance

    def append_df_to_excel(self, widget, **kwargs):

        Price_Enter = self.purchase_price_input.value
        NumberOfKg_Enter = self.number_kg_input.value
        Name = self.name_input.value
        if len(self.phone_input.value) == 0:
            Phone = self.phone_input.value
        if len(self.phone_input.value) == 11:
            Phone = self.phone_input.value
        else:
            pass
            # messagebox.showwarning('Warning', "Check length of Number")
            self.main_window.error_dialog('Warning', 'Check length of number')

        Debt = self.debt_input.value
        Credit = self.credit_input.value
        Clear_Option = self.cleared.value
        paymentMode = self.payment_method.value
        data = [[date_time, Name, str(Phone), str(Price_Enter), str(
            NumberOfKg_Enter), paymentMode, Clear_Option, str(Debt), str(Credit)]]
        DataTable = pd.DataFrame(data, columns=['Date', 'Name of Customer', 'Phone Number',
                                                'Amount Paid', 'Number of Kg', 'Payment Mode', 'Status', 'Debt', 'Credit'])
        # messagebox.showinfo('', "Successful!")
        self.main_window.confirm_dialog('Confirm', 'You are submiting this transaction to the database')

        try:
            DataTable.to_csv(self.database_path, mode='a',
                             index=False, header=False)
            # save the workbook
            # writer.save()
        except PermissionError:
            # messagebox.showerror(
            #     "Information", "Workbook is open. Please close workbook!")
            self.main_window.error_dialog(
                'Error', 'Workbook is open. Please close workbook!')
            return None

    def print_slip(self, widget, **kwargs):
        f = open('Print_slip.txt', 'w', encoding="utf-8")
        width = 30
        f.write('DYNAMO GAS INDUSTRIES'.center(width,
                ' ') + '\n')
        f.write('No.2 Dynamo Junction Ifite near Unizik Gate'.center(width,
                ' ') + '\n')
        f.write('Awka, Anambra State'.center(width,
                                       ' ') + '\n')
        f.write('07031399916, 07017770440, 07068068000'.center(width,
                                     ' ') + '\n')
        f.write('\n')
        f.write('Sales Receipt'.center(width, '-') + '\n')
        f.write(str(date_and_time)+'\n')
        f.write('\n')
        f.write('Transaction Details'.center(width, '-') + '\n')
        f.write('Customer: ' + str(self.name_input.value) + '\n')
        f.write('Phone Number: ' + str(self.phone_input.value) + '\n')
        f.write('\n')

        price_enter = self.purchase_price_input.value
        purchase_price = "₦"+str(price_enter)+'.00'
        #f.write('Price Per Kg: ' + str(purchase_price)+' Naira' + '\n')
        amountpaid = self.amount_paid_input.value
        moneypaid = "₦"+str(amountpaid)+'.00'

        trans_dict = {'Price/kg': str(self.price_perkg_input.value), 'Amount': str(
            moneypaid), 'Kg': str(self.number_kg_input.value) + 'kg', 'Price': str(purchase_price)}
        trans_table = pd.DataFrame(trans_dict, index=[1])

        trans_table = tabulate(trans_table, showindex=False,
                               headers=trans_table.columns)
        f.write(str(trans_table) + '\n')
        f.write('_______________________________________' + '\n')
        f.write('\n')
        balance = "%8.2f" % (float(amountpaid) - float(price_enter))
        f.write('Balance:' + '₦'+str(balance) + '\n')
        f.write('Debt:' + '₦' + str(self.debt_input.value) + '\n')
        f.write('Credit:' + '₦' + str(self.credit_input.value) + '\n')
        clear_option = self.cleared.value
        f.write('Status: ' + clear_option + '\n')
        f.close()
        if platform.system() == 'Windows':
            os.startfile("Print_slip.txt", "print")
        if platform.system()=='Darwin':
            printers_name=subprocess.getoutput("lpstat -a | awk '{print $1}'").split("\n")
            printer_name_list = []
            for printer_name in printers_name:
                printer_name_list.append(printer_name)
            
            self.printers_opt = toga.Selection(
            items= printer_name_list, style=Pack(flex=1, padding_left=100))

    def printWindow(self, widget, **kwargs):
        printer_label = toga.Label('Select a printer', style=Pack(padding_left=50, padding_top=25))

        os.system("lpr -P"+str(self.printers_opt.value)+"Print_slip.txt")
        self.printer_box.add(printer_label,self.printers_opt,self.ok_print)

        self.printer_window = toga.Window(title='Transaction Analysis')
        self.windows.add(self.printer_window)
        self.printer_window.content = self.printer_box
        self.printer_window.show()

    def EntryWindow(self, widget, **kwargs):
        self.entry_box = toga.Box(style=Pack(
            direction=COLUMN))  # e8aa42
        self.entry_box.add(self.transaction_entry_container)
        self.second_window = toga.Window(title='Transaction Entry')
        self.windows.add(self.second_window)
        self.second_window.content = self.entry_box
        self.second_window.show()

    def Analysis(self, widget, **kwargs):
        font_family = 'sans-serif'
        analysis_data = pd.read_csv(
            self.database_path, index_col='Date', parse_dates=True)
        #analysis_data = analysis_data.set_index('Date')
        selected_data = analysis_data.loc[str(self.date_input.value)]
        Revenue = "%8.2f" % selected_data['Amount Paid'].sum()

        kg_sold = "%8.2f" % selected_data['Number of Kg'].sum()

        cleared = len(
            selected_data[selected_data.Status == 'Cleared'])

        notcleared = len(
            selected_data[selected_data.Status == 'Not Cleared'])

        analyse_head = ['Key', 'Values']

        data = [('Revenue', '₦'+str(Revenue)), ('Kg Sold',
                                                str(kg_sold)+'kg'), ('Cleared', cleared), ('Not Cleared', notcleared)]
        self.analyse_table = toga.Table(analyse_head, data=data, missing_value='0', style=Pack(
            padding=5, font_family=font_family))
        self.trans_analyis_box.add(self.analyse_table)
        return self.trans_analyis_box

    def AnalysisWindow(self, widget, **kwargs):
        analyse_result_box = toga.Box(style=Pack(
            direction=COLUMN))
        analyse_result_box.add(self.tran_cont_box)
        self.third_window = toga.Window(title='Transaction Analysis')
        self.windows.add(self.third_window)
        self.third_window.content = analyse_result_box
        self.third_window.show()

    def Searchresult(self, widget, **kwargs):
        font_family = 'sans-serif'
        generaldata = pd.read_csv(
            self.database_path).astype(str)
        searched_data = generaldata[generaldata[str(
            self.searchby_opt.value)] == self.search_input.value]
        searched_data_rows = searched_data.to_numpy().tolist()

        analyse_head = list(searched_data.columns)

        data = searched_data_rows
        self.search_table = toga.Table(analyse_head, data=data, missing_value='0', style=Pack(
            padding=5, font_family=font_family))
        self.trans_analyis_box.add(self.search_table)
        return self.trans_analyis_box

    def delete_search_analysis_table(self, widget, **kwargs):
        self.trans_analyis_box.remove(self.analyse_table, self.search_table)


def main():
    return DynamoGas()


if __name__ == '__main__':
    main().main_loop()
