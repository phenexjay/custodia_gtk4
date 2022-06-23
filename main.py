 # -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Gtk.self.listbox()."""

import time

import gi
from datetime import datetime
from files import *

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')
gi.require_version('GtkSource', '5')
from gi.repository import Gio, Gtk, Gdk, Adw, Pango, GtkSource

PANE_POSITION = 345


class MainWindow(Gtk.ApplicationWindow):

    provider = Gtk.CssProvider.new()
    provider.load_from_file(Gio.File.new_for_path("./style/style.css"))
    
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, 500);
    languages = GtkSource.LanguageManager()  

    codeview_scrolled_window = Gtk.ScrolledWindow.new()  
     
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        
        self.set_title(title="Custodia Snippet Manager")
        self.set_default_size(width=int(1200), height=int(800))
        self.set_titlebar(titlebar=self.headerbar())
        self.set_child(self.main_stack())


    def headerbar(self):
        headerbar = Adw.HeaderBar.new()
        headerbar.set_show_start_title_buttons(True)
        box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
        button_open = Adw.SplitButton.new()
        button_open.set_label("Öffnen")
        button_open.connect("clicked", self.button_open_file)
        button_open.set_tooltip_text("Datei öffnen und Kollektion laden")
        box.append(button_open)

        button_new = Gtk.MenuButton.new()
        button_new.set_icon_name("document-new-symbolic")
        #button_new.connect("clicked", self.button_new_file)
        button_new.set_tooltip_text("Eine neue Kollektion erstellen")
        
        popover = Gtk.Popover()
        popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label.new("Kollektion benennen:")
        popover_box.append(label)
        popover.set_child(popover_box)
        button_new.set_popover(popover)
        box.append(button_new)

        box.append(Gtk.Separator()) 

        self.title = Adw.WindowTitle()
        self.title.set_title("Custodia Snippet Manager")
        self.title.set_subtitle("Keine Kollektion geöffnet")
        
        button_settings =Gtk.Button.new()
        button_settings.set_icon_name("menu-symbolic")
        button_settings.connect("clicked", self.button_open_file)
        button_settings.set_tooltip_text("Einstellungsfenster anzeigen")
        box.append(button_settings)

        headerbar.set_title_widget(self.title)
        headerbar.pack_start(box)
        
        return headerbar


    def main_stack(self):
    
        box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_homogeneous(homogeneous=False)

        # PAGE WELCOME
        self.page1 = self.main_stack_page_welcome()

        # PAGE CONTENT  
        self.page2 = self.main_stack_page_content()
        
        # PAGE SETTINGS 
        #self.page3 = self.main_stack_page_settings()

        self.stack = Gtk.Stack.new()
        self.stack.set_transition_type(transition=Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(duration=300)
        self.stack.add_titled(child=self.page1, name='welcome', title='Welcome')
        self.stack.add_titled(child=self.page2, name='content', title='Content')
        #stack.add_titled(child=self.page3, name='settings', title='Settings')
        
        self.stack.set_visible_child(self.page1)
        box.append(child=self.stack)
        
        return box


    def main_stack_page_welcome(self):
        
        # PAGE "WELCOME"
        page = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
   
        label = Gtk.Label()
        label.set_vexpand(True)
        label.set_label("Willkommen bei Custodia")
        label.set_valign(align=Gtk.Align.END)
        label.get_style_context().add_class("large-title")
        page.append(label)
        
        message = Gtk.Label()
        message.set_vexpand(True)
        message.set_label("\nDeine Verwaltung für Code-Schnipsel.\nUm zu beginnen, erstelle eine neue Kollektion,\noder öffne eine bereits bestehende.")
        message.get_style_context().add_class("heading")
        message.set_valign(align=Gtk.Align.START)
        message.set_justify(Gtk.Justification.CENTER)
        page.append(message)
         
        return page


    def main_stack_page_content(self):
        
        # PAGE "CONTENT"
        self.paned = Gtk.Paned()
        self.paned.set_vexpand(True)
        self.paned.set_position(PANE_POSITION)
        self.paned.set_shrink_start_child(False)
        self.paned.set_resize_start_child(False)
        self.paned.set_shrink_end_child(True)
        self.paned.set_resize_end_child(True)
        
        page = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        page.append(child=self.paned)
        
        # LEFT_PANE "SIDEBAR"        
        self.paned.set_start_child(self.listbox_categories())        
        self.paned.set_end_child(self.content_sourceview())

        return page


    def main_stack_page_settings(self):
        pass

 
    def listbox_categories(self, *args):
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_homogeneous(homogeneous=False)

        entry_box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        sidebar_entry = Gtk.Entry()
        sidebar_entry.connect("activate", self.listbox_add_category, sidebar_entry)
        sidebar_entry.set_hexpand(True)
        sidebar_entry.set_placeholder_text("Kategorie hinzufügen")
        sidebar_entry.set_has_frame(True)
        sidebar_entry.set_size_request(-1, 30)
        entry_box.append(sidebar_entry)
        
        button = Gtk.Button()
        button.set_icon_name("add-symbolic")
        button.connect("clicked", self.listbox_add_category, sidebar_entry)
        entry_box.append(button)
        
        entry_box.get_style_context().add_class("linked") 
        entry_box.set_margin_top(10)
        entry_box.set_margin_start(10)
        entry_box.set_margin_end(10)
        entry_box.set_margin_bottom(10)
        
        box.append(entry_box)
        box.append(Gtk.Separator())

        scrolled = Gtk.ScrolledWindow.new()
        scrolled.set_hexpand(True)
             
        scrolled_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.listbox = Gtk.ListBox.new()
        self.listbox.connect('row-activated', self.listbox_category_row_clicked)
        self.listbox.set_vexpand(True)

        scrolled_box.append(child=self.listbox)
      
        if self.data == None:
            pass
        else:
            for i in range(len(self.data) - 1):

                category_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                category_box.set_margin_start(10)
                category_box.set_margin_end(0)
                
                title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
                title_box.set_hexpand(True)
                title = Gtk.Label.new(str=str(self.data[i+1][0].title))
                title.set_hexpand(True)
                title.get_style_context().add_class("heading")
                title.set_halign(Gtk.Align.START)
                title.set_wrap(True)
                title.set_wrap_mode(Pango.WrapMode.WORD)
                title_box.append(title)

                button_delete = Gtk.Button()
                button_delete.set_icon_name("edit-delete-symbolic")
                button_delete.get_style_context().add_class("flat")
                button_delete.get_style_context().add_class("circular")
                button_delete.set_valign(Gtk.Align.START)
                button_delete.connect("clicked", self.button_delete_category, self.listbox, self.listbox.get_row_at_index(i), i)
                title_box.append(button_delete)   
                category_box.append(title_box)
                    
                created = Gtk.Label.new(str = "Erstellt am " + str(datetime.fromtimestamp(self.data[i+1][0].created).strftime("%d.%m.%y um %H:%M")))
                created.get_style_context().add_class("caption")
                created.get_style_context().add_class("dim-label")
                created.set_margin_bottom(5)
                created.set_halign(Gtk.Align.START)
                category_box.append(created)
                    
                counter = Gtk.Label.new(str = f"{len(self.data[i+1][1])} {'gespeicherter' if len(self.data[i+1][1]) == 1 else 'gespeicherte'} Schnipsel")
                counter.get_style_context().add_class("caption")
                counter.get_style_context().add_class("dim-label")
                counter.set_margin_bottom(10)
                counter.set_halign(Gtk.Align.START)
                category_box.append(counter)
                
                self.listbox.append(child=category_box)
                
                if i == 0:
                    self.listbox.get_row_at_index(i).set_margin_top(10)
                else:
                    self.listbox.get_row_at_index(i).set_margin_top(5)
                self.listbox.get_row_at_index(i).set_margin_bottom(5)
                self.listbox.get_row_at_index(i).set_margin_start(10)
                self.listbox.get_row_at_index(i).set_margin_end(10)
                self.listbox.get_row_at_index(i).set_name('listbox_cards')

        scrolled.set_child(scrolled_box)
        box.append(scrolled)
        
        box.append(Gtk.Separator())

        tag_list_box = Gtk.Grid()
        tag_list_box.set_size_request(-1, 200)

        if self.data != None:
            tag_list = self.tag_list_refresh()
            count = 0
            add = 0

            for i in range(len(tag_list)):
                i = 0
                j = 0
                add = 0
                
                while j < len(tag_list):
                    label = Gtk.Label.new()
                    label.set_label(tag_list[j])
                    label.set_halign(Gtk.Align.START)
                    label.set_valign(Gtk.Align.START)
                    if i == 0:
                        label.set_margin_start(5)
                    else:
                        label.set_margin_start(0)
                    label.set_margin_top(5)         
                    label.set_margin_end(5)
                    label.set_size_request(80, -1)
                    label.set_ellipsize(Pango.EllipsizeMode.END)
                    label.set_name("tags_list")

                    tag_list_box.attach(label, i, 0 + add, 1, 1)
                    i += 1
                    j += 1
                    if i == 4:
                        i = i - 4
                        add += 1
                    
            box.append(tag_list_box)
            
        return box


    def listbox_category_row_clicked(self, listbox, listboxrow):

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_homogeneous(homogeneous=False)
        box.set_vexpand(True)
        box.set_name("snippet_box")

        entry_box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        button = Gtk.Button()
        button.set_icon_name("go-previous")
        button.connect("clicked", self.button_return_to_categories)
        entry_box.append(button)
             
        sidebar_entry = Gtk.Entry()
        sidebar_entry.connect("activate", self.button_add_snippet, sidebar_entry, listbox, listboxrow)
        sidebar_entry.set_hexpand(True)
        sidebar_entry.set_placeholder_text("Schnipsel hinzufügen")
        sidebar_entry.set_has_frame(True)
        sidebar_entry.set_size_request(-1, 30)
        entry_box.append(sidebar_entry)
        
        button = Gtk.Button()
        button.set_icon_name("add-symbolic")
        #button.connect("clicked", self.sidebar_button_add_snippet, sidebar_entry)
        entry_box.append(button)
        
        entry_box.get_style_context().add_class("linked") 
        entry_box.set_margin_top(10)
        entry_box.set_margin_start(10)
        entry_box.set_margin_end(10)
        entry_box.set_margin_bottom(10)
        
        box.append(entry_box)
        
        separator = Gtk.Separator()
        box.append(separator)
        
        scrolled = Gtk.ScrolledWindow.new()
        scrolled.set_hexpand(True)
             
        scrolled_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.listbox = Gtk.ListBox.new()
        self.listbox.connect('row-activated', self.listbox_snippet_row_clicked, listboxrow.get_index())
        self.listbox.set_vexpand(True)
        
        scrolled_box.append(child=self.listbox)
        scrolled.set_child(box)

        for i in range(len(self.data[listboxrow.get_index() + 1][1])):
            snippet_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            snippet_box.set_margin_start(10)
            snippet_box.set_margin_end(0)
            
            title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            title_box.set_hexpand(True)
            
            title = Gtk.Label.new(str=self.data[listboxrow.get_index() + 1][1][i].title)
            
            title.set_hexpand(True)
            title.get_style_context().add_class("heading")
            title.set_halign(Gtk.Align.START)
            title.set_wrap(True)
            title.set_wrap_mode(Pango.WrapMode.WORD)
            title.set_name("title_box")
            title_box.append(title)

            button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

            button_edit = Gtk.Button()
            button_edit.set_icon_name("document-edit-symbolic")
            button_edit.get_style_context().add_class("flat")
            button_edit.get_style_context().add_class("circular")
            button_edit.set_valign(Gtk.Align.START)
            #button_edit.connect("clicked", self.button_edit_snippet, listbox, listboxrow, i)
            title_box.append(button_edit)  

            button_delete = Gtk.Button()
            button_delete.set_icon_name("edit-delete-symbolic")
            button_delete.get_style_context().add_class("flat")
            button_delete.get_style_context().add_class("circular")
            button_delete.set_valign(Gtk.Align.START)
            button_delete.connect("clicked", self.button_delete_snippet, listbox, listboxrow, i)
            button_box.append(button_delete)
            
            title_box.append(button_box)  
            snippet_box.append(title_box) 

            label_created = Gtk.Label.new(str = "Erstellt am " + str(datetime.fromtimestamp(int(self.data[listboxrow.get_index() + 1][1][i].created)).strftime("%d.%m.%Y um %H:%M")))
            label_created.get_style_context().add_class("caption")
            label_created.get_style_context().add_class("dim-label")
            label_created.set_margin_bottom(5)
            label_created.set_halign(Gtk.Align.START)

            snippet_box.append(label_created)
            
            tags_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)   
            tags_box.set_margin_bottom(10)
            tags = self.data[listboxrow.get_index() + 1][1][i].tags
            
            if tags == [] :
                label = Gtk.Label.new()
                label.set_label("Keine Tags")
                label.get_style_context().add_class("dim-label")
                label.get_style_context().add_class("caption")
                label.set_hexpand(True)
                label.set_halign(Gtk.Align.START)
                tags_box.append(label)
            else:    
                for j in range(len(tags)):
                    label = Gtk.Label.new()
                    label.set_label(tags[j])
                    label.set_name("tags")
                    tags_box.append(label)
                    
            snippet_box.append(tags_box)
            
            self.listbox.append(child=snippet_box)
            if i == 0:
                self.listbox.get_row_at_index(i).set_margin_top(10)
            else:
                self.listbox.get_row_at_index(i).set_margin_top(5)
            self.listbox.get_row_at_index(i).set_margin_bottom(5)
            self.listbox.get_row_at_index(i).set_margin_start(10)
            self.listbox.get_row_at_index(i).set_margin_end(10)
            self.listbox.get_row_at_index(i).set_name('listbox_cards')

        scrolled.set_child(scrolled_box)
        box.append(scrolled)
        self.paned.set_start_child(child=box)    
    

    def listbox_snippet_row_clicked(self, listbox, listboxrow, index):
        self.active_snippet = self.data[index + 1][1][listboxrow.get_index()]
        print(self.active_snippet)
        try:       
            buffer = self.content_sourceview.get_buffer()
            buffer.set_text(self.data[index + 1][1][listboxrow.get_index()].content)
            #print(self.active_snippet.content)
            adj = self.codeview_scrolled_window.get_vadjustment().set_value(0.0) 
        except:
            pass  


    def button_delete_category(self, button, listbox, listboxrow, index):
        del self.data[index+1]
        save_data(self.data)
        self.paned.set_start_child(self.listbox_categories())


    def button_delete_snippet(self, button, listbox, listboxrow, index):
        del self.data[listboxrow.get_index() + 1][1][index]
        self.listbox_category_row_clicked(listbox,listboxrow)
        save_data(self.data)


    def listbox_add_category(self, button, entry):
        self.data.append([category.Category(entry.get_text(), time.time()), [] ])

        entry.set_text("")
        save_data(self.data)
        self.paned.set_start_child(self.listbox_categories())


    def button_add_snippet(self, button, entry, listbox, listboxrow):
        print(self.data[listboxrow.get_index() + 1][1])
        self.data[listboxrow.get_index() + 1][1].append(snippet.Snippet(self.data[listboxrow.get_index() + 1][0].title, entry.get_text(), time.time()))
        
        entry.set_text("")
        save_data(self.data)
        self.listbox_category_row_clicked(listbox,listboxrow)

    
    def button_return_to_categories(self, button):
        #self.counter_snippets()
        self.paned.set_start_child(child=self.listbox_categories())
        
        
    def button_open_file(self, button):
        dialog = Gtk.FileChooserDialog()
        dialog.set_transient_for(self)
        dialog.set_title(title="Datei zum Öffnen auswählen")
        dialog.set_modal(modal=True)
        dialog.set_action(action=Gtk.FileChooserAction.OPEN)
        dialog.set_current_folder(Gio.File.new_for_path(path=str("./saves/")))

        dialog.add_button('Abbrechen', Gtk.ResponseType.CANCEL)
        dialog.add_button('Öffnen', Gtk.ResponseType.OK)
        dialog.connect('response', self.button_dialog_response)

        collection_filter = Gtk.FileFilter()
        collection_filter.set_name(name='Custodia Collection File')
        collection_filter.add_pattern(pattern="*.col")
        dialog.add_filter(collection_filter)

        all_filter = Gtk.FileFilter()
        all_filter.set_name(name='Alle Dateien anzeigen')
        all_filter.add_pattern(pattern='*')
        dialog.add_filter(filter=all_filter)
        
        select = dialog.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        select.get_style_context().add_class(class_name='suggested-action')

        cancel = dialog.get_widget_for_response(response_id=Gtk.ResponseType.CANCEL)
        cancel.get_style_context().add_class(class_name='destructive-action')
        
        dialog.show()


    def button_new_file(self, button):
        pass
        
                    
    def button_dialog_response(self, dialog, response):
        
        if response == Gtk.ResponseType.OK:                                               
            data = load_data(dialog.get_file().get_path())
            self.collection = data[0]
            self.data = data
            self.title.set_subtitle(f"Geöffnete Sammlung: {data[0]}")
            self.stack.set_visible_child(self.page2)
            self.paned.set_start_child(self.listbox_categories())    
        else: pass

        dialog.close()
        
        
    def content_sourceview(self):    
        box_sourceview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        self.tabview = Adw.TabView()
        self.tabview.add_page()
        
        self.tabbar = Adw.TabBar.new()
        self.tabbar.set_view(self.tabview)
        
        self.content_sourceview = GtkSource.View()
        self.content_sourceview.set_vexpand(True)
        self.content_sourceview.set_show_line_numbers(True)
        self.content_sourceview.set_show_right_margin(True)
        self.content_sourceview.set_highlight_current_line(True)
        self.content_sourceview.set_monospace(True)
        self.content_sourceview.set_editable(False)
        self.content_sourceview.set_cursor_visible(False)
        self.content_sourceview.set_highlight_current_line(False)
        #tabs = Pango.TabArray(1, True)
        #tabs.set_tab(0, Pango.TabAlign.TAB_LEFT, 4)
        #self.content_sourceview.set_tab(tabs)
        buffer = self.content_sourceview.get_buffer()
        buffer.set_language(self.languages.get_language("python"))
        self.codeview_scrolled_window.set_child(child=self.content_sourceview)
 
        box_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box_toolbar.set_margin_top(20)
        box_toolbar.set_margin_bottom(10)
        box_toolbar.set_margin_start(20)
        box_toolbar.set_margin_end(20)
        box_toolbar.get_style_context().add_class("toolbar")
        box_toolbar.get_style_context().add_class("osd")
        box_toolbar.set_hexpand(False)
        box_toolbar.set_valign(align=Gtk.Align.END)
        box_toolbar.set_halign(align=Gtk.Align.CENTER)  

        overlay = Gtk.Overlay()
        overlay.add_overlay(box_toolbar)
        overlay.set_child(child=self.codeview_scrolled_window)            
        
        self.button_edit = Gtk.ToggleButton.new()
        self.button_edit.set_icon_name("document-edit-symbolic")
        self.button_edit.get_style_context().add_class("flat")
        self.button_edit.get_style_context().add_class("circular")
        self.button_edit.connect("toggled", self.content_button_edit_snippet)
        box_toolbar.append(self.button_edit)

        button_copy = Gtk.Button.new()
        button_copy.set_icon_name("edit-copy-symbolic")
        button_copy.get_style_context().add_class("flat")
        button_copy.get_style_context().add_class("circular")
        box_toolbar.append(button_copy)

        button_print = Gtk.Button.new()
        button_print.set_icon_name("printer-symbolic")
        button_print.get_style_context().add_class("flat")
        button_print.get_style_context().add_class("circular")
        box_toolbar.append(button_print)
        
        button_delete = Gtk.Button.new()
        button_delete.set_icon_name("edit-delete-symbolic")
        button_delete.get_style_context().add_class("flat")
        button_delete.get_style_context().add_class("circular")
        button_delete.get_style_context().add_class("destructive-action")
        box_toolbar.append(button_delete)
                
        box_sourceview.append(overlay)
    
        return box_sourceview


    def content_button_edit_snippet(self, button):
        
        widget = self.content_sourceview
        buffer = widget.get_buffer()   

        if self.button_edit:

            widget.set_editable(True)
            widget.set_cursor_visible(True)
            widget.set_highlight_current_line(True)
            #widget.set_background_pattern(True)
            widget.set_show_right_margin(True)
            self.button_edit = False 
        else:
            self.active_snippet.content = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), include_hidden_chars=True)          
            widget.set_editable(False)
            widget.set_cursor_visible(False)
            widget.set_highlight_current_line(False)
            self.button_edit = True
            
            save_data(self.data)        


    def tag_list_refresh(self):
        tags = []    
        for i in range(len(self.data) - 1):
            for j in range(len(self.data[i + 1])):
                #print(self.data[i + 1][1][j].tags)
                try:
                    temp_data = self.data[i + 1][1][j].tags
                    if temp_data != None:
                        for item in temp_data:
                            if item not in tags:
                                tags.append(item)
                        
                    temp_data = None
                except IndexError: pass
                
        return tags
            
            
        
        
class Application(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Adw.Application.do_startup(self)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def do_shutdown(self):
        Adw.Application.do_shutdown(self)


if __name__ == '__main__':
    import sys

    app = Application()
    app.run(sys.argv)
