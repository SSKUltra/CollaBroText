import sublime, sublime_plugin
from .datastructure_plugin import *
global layout_flag 
global layout_region

#layout_flag is used to check if layout is open or not and
#layout_region used to determine which region the layout corresponds to 
layout_flag = False
layout_region = "0"

#class used to add the highlighted region to the file 
class AddRegionCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		for region in self.view.sel():
			
			self.view.add_regions('y', [region], 'comment', 'dot', sublime.HIDE_ON_MINIMAP)
			#print("done")

# class printer(sublime_plugin.EventListener):
# 	def on_selection_modified(self,view):
# 		for region in view.sel():
# 			print(region)

#Command runs when cursor position is changed. Displays comments corresponding to the region in file
#NEED TO FIX HIGHLIGHT AFTER CLOSING LAYOUT 
class HighlightChange(sublime_plugin.EventListener):
	def on_selection_modified(self,view):
		global layout_flag
		global layout_region
		global comment

		#need window obj to call other commands
		window = sublime.active_window()
		UUID = ['x', 'y']
		current_view_obj = view

		#change color of all regions to 'comment' ignoring the region currently open
		for id in UUID:
			if layout_region != id and layout_region != "0":

				region1 = view.get_regions(id)
				view.add_regions(id, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)

		#if current cursor position is contained in a region in file and no layout is open then open layout 
		for id in UUID:
			region2 = view.get_regions(id)
			for region in view.sel():
				if region2[0].contains(region):
					view.add_regions(id, region2, 'string', 'dot', sublime.HIDE_ON_MINIMAP)

					if layout_region != id and layout_region != "0":
						window.run_command("close_view")


					if layout_flag == False :

						layout_flag = True
						layout_region = id
						comment = id
						command_name = "set_layout"
						command_arguments = { "cols": [0, 0.72, 1.0],"rows": [0.0,1.0],"cells": [ [0, 0, 1, 1], [1,0,2,1] ]	}
						window.run_command(command_name, command_arguments)
						window.run_command("display_user_input")
		window.focus_view(current_view_obj)
		
		#fixed the dual highlight problem
		for id in UUID:
			if layout_region != id and layout_region != "0":

				region1 = view.get_regions(id)
				view.add_regions(id, region1, 'comment', 'dot', sublime.HIDE_ON_MINIMAP)


#displays content from the datastructure
class DisplayUserInputCommand(sublime_plugin.TextCommand):
	def run(self,edit):

		global comment_view_obj
		global comment

		comment_view_obj = self.view
		comment = "testing for : " + comment 
		#window.focus_view(comment_view_obj)
		self.view.insert(edit, 0, comment)
		self.view.set_scratch(True)
		self.view.set_read_only(True)

#keybind ctrl+shft+4 to close the layout manually
class CloseViewCommand(sublime_plugin.WindowCommand):
	def run(self):

		global comment_view_obj
		global layout_flag
		global layout_region
		layout_flag = False
		layout_region = "0"
		self.window.focus_view(comment_view_obj)
		self.window.run_command("close_file")

		command_name = "set_layout"
		command_arguments = { "cols": [0, 1.0],"rows": [0.0,1.0],"cells": [ [0, 0, 1, 1], ] }
		self.window.run_command(command_name, command_arguments)	
	
