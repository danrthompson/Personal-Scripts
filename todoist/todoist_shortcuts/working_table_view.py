import sys
from notifications import send_notification, Notification
import pyto_ui as ui


view = ui.View()
view.background_color = ui.COLOR_SYSTEM_BACKGROUND


cells = []

cell = ui.TableViewCell()
cell.text_label.text = "cell1"
cells.append(cell)

cell = ui.TableViewCell()
cell.text_label.text = "cell1"
cells.append(cell)

section = ui.TableViewSection("sec", cells)

selected_cells = set()


def selected_cb(section: ui.TableViewSection, index: int):
    cell = section.cells[index]
    if index in selected_cells:
        selected_cells.remove(index)
        cell.accessory_type = ui.ACCESSORY_TYPE_NONE
        return

    selected_cells.add(index)
    cell.accessory_type = ui.ACCESSORY_TYPE_CHECKMARK


section.did_select_cell = selected_cb


table = ui.TableView(style=ui.TABLE_VIEW_STYLE_GROUPED, sections=[section])

# view.add_subview(table)

ui.show_view(table, ui.PRESENTATION_MODE_SHEET)

print(selected_cells)
