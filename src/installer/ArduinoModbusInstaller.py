import wx
#import wx.xrc
import os
import psutil
import shutil
import zipfile
import socket
import xml.etree.ElementTree as et
from subprocess import Popen, PIPE

class AppWindow(wx.Frame):
	MAC_VENDOR_ID = '86-1a-30'
	dir_changed = False

	def __init__(self):
		wx.Frame.__init__(self, None, id = wx.ID_ANY, title = 'Arduino Modbus Installer', pos = wx.DefaultPosition, size = wx.Size(500,233), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		fgSizer1 = wx.FlexGridSizer(5, 1, 0, 0)
		fgSizer1.SetFlexibleDirection(wx.BOTH)
		fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

		bSizer4 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, 'Arduino Modbus Installer', wx.DefaultPosition, wx.Size(500,60), wx.ALIGN_CENTER_HORIZONTAL)
		self.m_staticText3.Wrap(-1)

		self.m_staticText3.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))

		bSizer4.Add(self.m_staticText3, 0, wx.ALL, 5)

		fgSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

		bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, 'Mach4 Directory:', wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText1.Wrap(-1)

		bSizer1.Add(self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		self.mach_dir_url = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300,-1), wx.TE_READONLY)
		bSizer1.Add(self.mach_dir_url, 0, wx.ALL, 5)

		self.btn_browse = wx.Button(self, wx.ID_ANY, 'Browse', wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer1.Add(self.btn_browse, 0, wx.ALL, 5)

		fgSizer1.Add(bSizer1, 1, wx.EXPAND, 5)

		bSizer2 = wx.BoxSizer(wx.VERTICAL)

		bSizer2.Add((0, 10), 1, wx.EXPAND, 5)

		fgSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

		bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, 'Select Profile:      ', wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText2.Wrap(-1)

		bSizer3.Add(self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		self.cbo_profile_selection = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(180,-1), [], wx.CB_READONLY)
		bSizer3.Add(self.cbo_profile_selection, 0, wx.ALL, 5)

		bSizer3.Add((50, 0), 1, wx.EXPAND, 5)

		self.adc_checkbox = wx.CheckBox(self, wx.ID_ANY, u"ADC", wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.adc_checkbox, 0, wx.ALL, 5)

		bSizer3.Add((25, 0), 1, wx.EXPAND, 5)

		self.dac_checkbox = wx.CheckBox(self, wx.ID_ANY, u"DAC", wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer3.Add(self.dac_checkbox, 0, wx.ALL, 5)

		bSizer3.Add((50, 0), 1, wx.EXPAND, 5)

		fgSizer1.Add(bSizer3, 1, wx.EXPAND, 5)
		
		bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Arduino IP Address: ", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText4.Wrap(-1)

		bSizer5.Add(self.m_staticText4, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		ip_address = '' #self.get_device_ip()
		self.ip_address_entry = wx.TextCtrl(self, wx.ID_ANY, ip_address, wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer5.Add(self.ip_address_entry, 0, wx.ALL, 5)


		bSizer5.Add((0, 0), 1, wx.EXPAND, 5)
		self.btn_install = wx.Button(self, wx.ID_ANY, 'Install', wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer5.Add(self.btn_install, 0, wx.ALL, 5)


		fgSizer1.Add(bSizer5, 1, wx.EXPAND, 5)

		self.SetSizer(fgSizer1)
		self.Layout()

		self.Centre(wx.BOTH)

		# event binders
		self.btn_browse.Bind(wx.EVT_BUTTON, self.btn_browse_on_click)
		self.btn_install.Bind(wx.EVT_BUTTON, self.btn_install_on_click)
		self.cbo_profile_selection.Bind(wx.EVT_UPDATE_UI, self.update_profile_choices)

		self.Show()
		self.find_default_mach_installation()

	def get_device_ip(self):
		ip_addr = ''
		pid = Popen(['arp', '-a'], stdout=PIPE)
		cmd_out = pid.communicate()[0].decode('utf-8').split()

		idx = -1
		for i in cmd_out:
			if self.MAC_VENDOR_ID in i:
				break
			idx += 1

		if cmd_out[idx]:
			ip_addr = cmd_out[idx]

		return ip_addr

	def find_default_mach_installation(self):
		root_dir = os.path.abspath(os.sep)
		for folder in os.listdir(root_dir):
			if 'Mach4' in folder:
				self.mach_dir_url.ChangeValue(os.path.join(root_dir, folder))
				self.dir_changed = True
				break

	def update_profile_choices(self, event):
		if self.dir_changed:
			self.dir_changed = False
			mach_dir = self.mach_dir_url.GetValue()
			profile_dir = os.path.join(mach_dir, 'Profiles')
			
			profile_choices = ['']
			for profile in os.listdir(profile_dir):
				profile_choices.append(profile)

			self.cbo_profile_selection.Clear()
			self.cbo_profile_selection.Append(profile_choices)
			self.cbo_profile_selection.SetSelection(0)
		event.Skip()

	def btn_browse_on_click(self, event):
		dlg = wx.DirDialog(None, "Choose Mach4 installation directory", "", wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST)
		res = dlg.ShowModal()
		if res == wx.ID_OK:
			file_path = dlg.GetPath()
			self.mach_dir_url.ChangeValue(file_path)
			self.dir_changed = True
		event.Skip()

	def dict_to_machine_ini(self, ini_dict, out_loc):
		with open(out_loc, 'w') as out_file:
			for item in ini_dict:
				out_file.write('[{0}]\n'.format(item))
				properties_dict = ini_dict[item]

				if properties_dict:
					for prop in properties_dict: 
						out_file.write('{0}={1}\n'.format(prop, properties_dict[prop]))
	

	def machine_ini_to_dict(self, ini_loc):
		main_dict = {}
		nested_dict = {}
		heading = ''
		last_line = ''

		with open(ini_loc, 'r') as ini_file:
			for line in ini_file:
				if not line.strip():
					continue

				if '[' in last_line and not '=' in last_line:
					main_dict[heading] = None
					
				if '[' in line and not '=' in line:			
					if nested_dict: 
						main_dict[heading] = nested_dict
						nested_dict = {}
					heading = line.strip('[]\r\n')
				else:
					line = line.rstrip('\r\n').split('=')
					sub_heading = line[0]
					value = line[1]
					nested_dict[sub_heading] = value

				last_line = line

		if nested_dict: 
			main_dict[heading] = nested_dict
			nested_dict = {}

		return main_dict

	def is_valid_ipv4_address(self, address):
		try:
		    socket.inet_pton(socket.AF_INET, address)
		except AttributeError:  # no inet_pton here, sorry
		    try:
		        socket.inet_aton(address)
		    except socket.error:
		        return False
		    return address.count('.') == 3
		except socket.error:  # not a valid address
		    return False

		return True

	def mach_is_running(self):
		# check if Mach4 is running
		mach_running = False

		for process in psutil.process_iter():
			if 'Mach4' in process.name():
				mach_running = True
				wx.MessageBox("Mach4 is currently running. \nPlease close Mach4 and try again.", "Confirm", wx.OK)

		return mach_running

	def backup_machine_ini(self, ini_path, backup_path):
		# make a backup of Machine.ini
		if self.cbo_profile_selection.GetSelection() != 0:			
			try:
				shutil.copy(ini_path, backup_path)
			except Exception as e:
				print('failed to copy file \n {0}'.format(e))

	def enable_plugin_in_ini(self, ini_dict, plugin_name):
		test_val = ini_dict.get('Plugins', None)
		if test_val is None:
			ini_dict['Plugins'] = {}
		ini_dict['Plugins'][plugin_name] = 1
				
	def create_modbus_device(self, ini_dict, dev_name):
		dev_id = 0
		if 'ModbusDevices' in ini_dict:
			if ini_dict['ModbusDevices'] is not None:
				dev_id = len(ini_dict['ModbusDevices'])
			else:
				ini_dict['ModbusDevices'] = {}
		else:
			ini_dict['ModbusDevices'] = {}			

		if not dev_name in ini_dict['ModbusDevices'].values():
			ini_dict['ModbusDevices']['Dev{0}'.format(dev_id)] = dev_name

		ini_dict['ModbusDevice'] = None

	def create_global_registers(self, ini_dict): 
		inc = 1
		# find the last index of gReg attribute
		for properties in ini_dict:
			if 'gReg' in properties:
				inc += 1

		# update ini_dict with gReg device settings from file
		modbus_ini_dict = self.machine_ini_to_dict('gReg_ini_settings')
		temp = {}

		# add gReg values to ini_dict without overwriting any current registers 
		for reg_old_val in modbus_ini_dict:
			reg_new_val = ''.join([i for i in str(reg_old_val) if not i.isdigit()])
			reg_new_val += str(inc)
			temp[reg_new_val] = modbus_ini_dict[reg_old_val]
			inc += 1

		ini_dict.update(temp)

	def get_modbus_ini_settings(self):
		modbus_settings = 'modbus_ini_settings'
		if self.adc_checkbox.IsChecked():
			modbus_settings += '_adc'
		if self.dac_checkbox.IsChecked():
			modbus_settings += '_dac'
		return modbus_settings

	def btn_install_on_click(self, event):
		mach_dir = self.mach_dir_url.GetValue()
		ini_path = backup_path = ''
		profile = self.cbo_profile_selection.GetValue()
		ini_path = os.path.join(mach_dir, 'Profiles\\{0}\\Machine.ini'.format(profile))
		backup_path = os.path.join(mach_dir, 'Profiles\\{0}\\Backups\\Machine.ini.bak'.format(profile))
		
		if self.mach_is_running():
			return

		self.backup_machine_ini(ini_path, backup_path)

		ini_dict = self.machine_ini_to_dict(ini_path)
		 
		#  enable modbus and regfile plugins
		self.enable_plugin_in_ini(ini_dict, 'mcModbus')

		# create modbus device
		self.create_modbus_device(ini_dict, 'Arduino')

		# update ini_dict with modbus device settings from file
		modbus_settings = self.get_modbus_ini_settings()
		print(modbus_settings)
		modbus_ini_dict = self.machine_ini_to_dict(modbus_settings)
		ini_dict.update(modbus_ini_dict)

		# validate IP address and add to ini_dict
		ip_addr = self.ip_address_entry.GetValue().strip()

		if not self.is_valid_ipv4_address(ip_addr):
			wx.MessageBox("Invalid IP Address Entered! \n Aborting Installation.", "Error", wx.OK)
			return

		ini_dict['ModbusDevice/Arduino']['IPAddr'] = ip_addr

		# write the edited Machine.ini into the Mach4 Profiles directory
		self.dict_to_machine_ini(ini_dict, ini_path)
		
		wx.MessageBox("Installation complete!", "Confirm", wx.OK)

		event.Skip()

	def __del__(self):
		pass

app = wx.App()
frame = AppWindow()
app.MainLoop()