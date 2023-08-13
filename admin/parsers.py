import os

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from admin.dataclasses import ExcelDish, ExcelMenu, ExcelSubmenu


def parse_excel(file: str, sheet_name: str = 'Лист1') -> list[dict]:
    """Возвращает список ExcelMenus в виде list[dict]"""
    excel_path = rf'{os.path.dirname(__file__)}/{file}'
    book: Workbook = load_workbook(excel_path)
    sheet: Worksheet = book.get_sheet_by_name(sheet_name)
    res = []
    cur = 1
    while True:
        menu_name = sheet.cell(cur, 2).value
        menu_descr = sheet.cell(cur, 3).value
        if isinstance(menu_name, str) and isinstance(menu_descr, str):
            cur += 1
            cur_menu = ExcelMenu(title=menu_name, description=menu_descr, submenus=[])
            res.append(cur_menu)
            while True:
                submenu_name = sheet.cell(cur, 3).value
                submenu_descr = sheet.cell(cur, 4).value
                if isinstance(submenu_name, str) and isinstance(submenu_descr, str):
                    cur += 1
                    cur_submenu = ExcelSubmenu(
                        title=submenu_name, description=submenu_descr, dishes=[]
                    )
                    cur_menu.submenus.append(cur_submenu)
                    while True:
                        dish_name = sheet.cell(cur, 4).value
                        dish_descr = sheet.cell(cur, 5).value
                        dish_price = sheet.cell(cur, 6).value
                        dish_discount = sheet.cell(cur, 7).value
                        if dish_name and dish_descr and dish_price:
                            dish_price = (
                                dish_price * (1 - dish_discount)
                                if dish_discount and (0 < dish_discount < 1)
                                else dish_price
                            )
                            cur += 1
                            cur_submenu.dishes.append(
                                ExcelDish(
                                    title=dish_name,
                                    description=dish_descr,
                                    price=dish_price,
                                )
                            )
                        else:
                            break
                else:
                    break
        else:
            break
    res_dict = [menu.as_dict for menu in res]
    return res_dict
