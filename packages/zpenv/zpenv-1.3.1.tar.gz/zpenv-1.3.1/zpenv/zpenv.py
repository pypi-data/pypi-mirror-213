import subprocess
import zpp_args
from zpp_config import Config
import venv
import os
import sys
import json
from datetime import datetime
import shutil
import psutil

import locale

#Calcul du chemin d'un fichier
def path_reg(arg):
	if os.path.isabs(arg):
		return arg
	return os.path.abspath(arg)

#Cherche le terminal (cmd,powershell,bash...) sur lequel est exécuté l'app
def get_os():
	if os.name=="nt":
		try:
			if "zpenv" not in psutil.Process(os.getppid()).name():
				return psutil.Process(os.getppid()).name()
			else:
				return psutil.Process(psutil.Process(os.getppid()).ppid()).name()
		except:
			return "cmd"
		#return os.popen(f'powershell.exe -Command "ps -Id {PID} | Select-Object -ExpandProperty Name"').read().strip()
	else:
		try:
			return os.popen(f'ps -p {os.getppid()} -o comm=').read().strip()
		except:
			return "linux"

def lang(data, local = locale.getdefaultlocale()[0]):
	if local=="fr_FR":
		return data[0]
	else:
		return data[1]

#Création du context
class Context:
	def __init__(self, virtdir, virtname=None, prompt=None):
		self.env_dir = virtdir
		if virtname==None:
			name = virtdir.split(path_rep[0])
			self.env_name = name[len(name)-1]
		else:
			self.env_name = virtname
		if prompt!=None:
			self.prompt = f'({prompt}) '
		else:
			self.prompt = f'({self.env_name}) '
		self.executable = sys.executable
		self.python_dir = os.path.dirname(sys.executable)
		self.python_exe = sys.executable.replace(self.python_dir,"").replace(path_rep[0],"")
		self.inc_path = virtdir + path_rep[0] +'Include'
		self.lib_path = virtdir + path_rep[0] +'Lib'
		self.bin_path = virtdir + path_rep[0] +'Scripts'
		self.bin_name = 'bin'
		if sys.platform == 'win32':
			self.bin_name = 'Scripts'
		self.env_exe = self.bin_path + path_rep[0] + self.python_exe
		self.env_exec_cmd = self.env_exe
		self.cfg_path = virtdir + path_rep[0] + 'pyvenv.cfg'

#Affiche les logs
def print_log(message):
	if not argument.nolog:
		if argument.nodate:
			print(message)
		else:
			date = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
			print(f"[{date}] - {message}")

#Ajoute l'environnement dans le fichier de config
def add_venv(data):
	if os.path.exists(argument.configfile):
		with open(argument.configfile, 'r') as file:
			content = file.read()
			try:
				content = json.loads(content)
			except:
				print_log(lang(["ERREUR: Fichier de config corrompu","ERROR: Config file corrupted"]))
				return
	else:
		content = {}

	content[data['env_name']] = data
	content = json.dumps(content, indent=4)
	
	with open(argument.configfile, 'w') as file:
		file.write(content)

#Supprime l'environnement du fichier de config
def del_venv(envname):
	if os.path.exists(argument.configfile):
		with open(argument.configfile, 'r') as file:
			content = file.read()
			try:
				content = json.loads(content)
			except:
				print_log(lang(["ERREUR: Fichier de config corrompu","ERROR: Config file corrupted"]))
				return
	else:
		content = {}

	if envname in content:
		del content[envname]
		content = json.dumps(content, indent=4)
		
		with open(argument.configfile, 'w') as file:
			file.write(content)
		print_log(lang(["Environnement supprimé du fichier de config","Environnement remove from config file"]))
	else:
		print_log(lang(["Environnement non trouvé dans le fichier de config","Environnement not found in config file"]))


#Supprime l'environnement du fichier de config
def edit_venv(envname, key, value):
	if os.path.exists(argument.configfile):
		with open(argument.configfile, 'r') as file:
			content = file.read()
			try:
				content = json.loads(content)
			except:
				print_log(lang(["ERREUR: Fichier de config corrompu","ERROR: Config file corrupted"]))
				return
	else:
		content = {}

	if envname in content:
		content[envname][key]=value
		content = json.dumps(content, indent=4)
		
		with open(argument.configfile, 'w') as file:
			file.write(content)
		print_log(lang(["Environnement edité","Environnement edited"]))
	else:
		print_log(lang(["Environnement non trouvé dans le fichier de config","Environnement not found in config file"]))

#Recherche l'environnement dans le fichier de config
def load_venv(name):
	if os.path.exists(argument.configfile):
		with open(argument.configfile, 'r') as file:
			content = file.read()
			try:
				content = json.loads(content)
				if name in content:
					return content[name]
			except:
				print_log(lang(["ERREUR: Fichier de config corrompu","ERROR: Config file corrupted"]))
				return None
	return False

#Check si le package est déjà installé
def get_package(binpath,namemodule):
	cmd = [binpath, '-m', 'pip', 'freeze']
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	for pack in stdout.decode().split("\r\n"):
		if namemodule.replace("_","-")+"==" in pack:
			return True
	return False

#Installation d'un module dans un environnement
def install_module(binpath,namemodule,proxy):
	if get_package(binpath, namemodule):
		print_log(lang([f"Module {namemodule} déjà installé",f"Module {namemodule} already installed"]))
		return
	
	cmd = [binpath, '-m', 'pip', 'install', namemodule]
	if proxy!=None:
		cmd.append('--proxy='+proxy)
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while True:
		output = proc.stdout.readline().decode("utf-8").strip()
		if output == "":
			break
		print_log(output)

	d_error = False
	#Pour éviter les erreurs sur un pip pas à jour
	if "A new release of pip available" not in proc.stderr.read().decode("utf-8").strip():
		proc.stderr.seek(0)
		for output in proc.stderr.readlines():
			if len(output)>0 and d_error==False:
				logs(f"ERREUR: Module {namemodule} non installé\nMessage d'erreur: {output.decode()}", "error")
				d_error=True

			print_log(output.decode("utf-8").strip(), "error")

#Suppression d'un module dans un environnement
def remove_module(binpath,namemodule):
	if not get_package(binpath, namemodule):
		print_log(lang([f"Module {namemodule} non installé",f"Module {namemodule} not installed"]))
		return
	
	cmd = [binpath, '-m', 'pip', 'uninstall', '-y', namemodule]
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while True:
		output = proc.stdout.readline().decode("utf-8").strip()
		if output == "":
			break

		print_log(output)

	d_error = False

	proc.stderr.seek(0)
	for output in proc.stderr.readlines():
		if len(output)>0 and d_error==False:
			print_log(lang([f"ERREUR: Module {namemodule} non supprimé\nMessage d'erreur: {stderr.decode()}",f"ERROR: Module {namemodule} not deleted\nError message: {stderr.decode()}"]))
			d_error=True

		print_log(output.decode("utf-8").strip(), "error")

	
	
#Upgrade d'un module dans un environnement
def upgrade_module(binpath,namemodule,proxy):
	if not get_package(binpath, namemodule):
		print_log(lang([f"Module {namemodule} non installé",f"Module {namemodule} not installed"]))
		return

	cmd = [binpath, '-m', 'pip', 'install', namemodule, '--upgrade']
	if proxy!=None:
		cmd.append('--proxy='+proxy)

	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while True:
		output = proc.stdout.readline().decode("utf-8").strip()
		if output == "":
			break

		print_log(output)

	d_error = False
	#Pour éviter les erreurs sur un pip pas à jour
	if "A new release of pip available" not in proc.stderr.read().decode("utf-8").strip():
		proc.stderr.seek(0)
		for output in proc.stderr.readlines():
			if len(output)>0 and d_error==False:
				print_log(lang([f"ERREUR: Module {namemodule} non mis à jour\nMessage d'erreur: {stderr.decode()}",f"ERROR: Module {namemodule} not updated\nError message: {stderr.decode()}"]))
				d_error=True

			print_log(output.decode("utf-8").strip(), "error")


def main():
	parse = zpp_args.parser()
	parse.set_description(lang(["Gestionnaire d'environnement virtuel","Virtual environment manager"]))
	parse.set_argument(longname="install", description=lang(["Installer l'environnement","Install environment"]), default=False)
	parse.set_argument(longname="remove", description=lang(["Supprimer un environnement","Remove environment"]), default=False)
	parse.set_argument(longname="migrate", description=lang(["Migrer un environnement existant","Migrate an existing environment"]), default=False)
	parse.set_argument("l", longname="list", description=lang(["Lister les environnement","List environments"]), default=False)
	parse.set_argument("I", longname="info", description=lang(["Informations sur un environnement","Information about an environment"]), default=False)
	parse.set_argument("o", longname="open", description=lang(["Ouvrir un environnement","Open environment"]), default=False)
	parse.set_argument(longname="shell", description=lang(["Ouvrir l'environnement en mode shell","Open environment in shell mode"]), default=False)
	parse.set_argument("i", longname="installmodule", description=lang(["Installer des modules","Install modules"]), store="value", default=None, category="Package management")
	parse.set_argument("r", longname="removemodule", description=lang(["Supprimer des modules","Remove modules"]), store="value", default=None, category="Package management")
	parse.set_argument("u", longname="upgrademodule", description=lang(["Upgrade de module","Upgrade module"]), store="value", default=None, category="Package management")
	parse.set_argument("R", longname="requirement", description=lang(["Installer module depuis fichier requirement","Install module from requirement file"]), store="value", default=None, category="Package management")
	parse.set_argument(longname="proxy", description=lang(["Utiliser un proxy pour les installations","Use a proxy for installations"]), store="value", default=None, category="Package management")
	parse.set_argument(longname="local", description=lang(["Utiliser le fichier zpenv.cfg du répertoire courant","Use the zpenv.cfg file from the current directory"]), default=None)
	parse.set_argument(longname="configfile", description=lang(["Fichier de configuration des environnements","Environments configuration file"]), store="value", default=None)
	parse.set_argument(longname="nodate", description=lang(["Désactiver l'affichage de la date dans les logs","Disable date in the logs"]), default=False)
	parse.set_argument(longname="nolog", description=lang(["Désactiver l'affichage des logs","Disable display of logs"]), default=False)

	parse.set_argument("n", longname="name", description=lang(["Nom de l'environnement","Environment name"]), store="value", default=None, category="Install")
	parse.set_argument("S", longname="sitepackages", description=lang(["Accorde l'accès au system site-packages dir","Grant access to the system site-packages dir"]), default=False, category="Install")
	if os.name != 'nt':
		parse.set_argument("s", longname="symlinks", description=lang(["Tenter d'utiliser un symlink","Attempt to use a symlink"]), default=False, category="Install")
	parse.set_argument("C", longname="clear", description=lang(["Nettoyer le dossier de l'environnement","Clear environment folder"]), default=False, category="Install")
	parse.set_argument(longname="upgradepython", description=lang(["Mettre à jour la version de python","Upgrade Python version"]), default=False, category="Install/Management")
	parse.set_argument(longname="installpip", description=lang(["Installer pip","Install pip"]), default=None, category="Install/Management")
	parse.set_argument("U", longname="upgradepip", description=lang(["Mettre à jour pip pendant l'installation","Upgrade pip during installation"]), default=False, category="Install")
	parse.set_argument("p", longname="nopip", description=lang(["Ne pas installer pip","Do not install pip"]), default=False, category="Install")
	parse.set_argument(longname="prompt", description=lang(["Spécifier le message du prompt","Specify prompt message"]), store="value", default=None, category="Install")
	parse.set_argument("t", longname="tag", description=lang(["Ajouter/Lister des tags","Add/List tags"]), store="value", default=None, category="Install/Management")
	parse.set_argument("c", longname="comment", description=lang(["Ajouter un commentaire","Add a comment"]), store="value", default=None, category="Install/Management")
	parse.set_argument("D", longname="projectfolder", description=lang(["Spécifier un dossier de projet","Specify a project folder"]), store="value", default=None, category="Install/Management")
	parse.set_argument(longname="removecomment", description=lang(["Supprimer un commentaire","Remove a comment"]), default=None, category="Install/Management")
	parse.set_argument(longname="removetag", description=lang(["Supprimer un tag","Remove a tag"]), store="value", default=None, category="Install/Management")

	parse.set_argument(longname="nopurge", description=lang(["Ne supprime pas le dossier de l'environnement","Does not delete environment folder"]), default=False, category="Remove")
	parse.set_parameter("VENV_NAME", description=lang(["Nom de l'environnement virtuel","Virtual environment name"]))
	parse.disable_check()
	global argument
	parameter, argument = parse.load()

	global path_rep
	if os.name=='nt':
	    path_rep = ["\\","/"]
	else:
	    path_rep = ["/","\\"]

	if parameter!=None and argument!=None:
		if argument.local:
			argument.configfile = 'zpenv.cfg'
		if argument.configfile==None:
			argument.configfile = os.path.split(__file__)[0] + path_rep[0] + 'zpenv.cfg'

		if argument.install:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				print_log(lang(["Création du contexte","Create context"]))
				virtdir = path_reg(paramenv)
				context = Context(virtdir, argument.name, argument.prompt)

				envc = load_venv(context.env_name)
				if envc==False:
					if os.path.exists(virtdir) and os.path.isdir(virtdir) and len(os.listdir(virtdir))!=0:
						ch = input(lang(["Le dossier n'est pas vide. Nettoyer ? (y/N)","Folder is not empty. Clear ? (y/N)"]))
						if ch=="y":
							argument.clear=True
						else:
							sys.exit()
					
					if os.name == 'nt':
						argument.symlinks = False

					if argument.clear and argument.upgradepython:
						print_log(lang(['vous ne pouvez pas fournir --upgrade et --clear ensemble','you cannot supply --upgrade and --clear together']))
					
					if argument.nopip and argument.installmodule!=None:
						print_log(lang(['vous ne pouvez pas fournir --nopip et --installmodule ensemble','you cannot supply --nopip and --installmodule together']))
					
					print_log(lang(["Init builder","Init builder"]))
					virtual = venv.EnvBuilder(system_site_packages=argument.sitepackages, clear=argument.clear, symlinks=argument.symlinks, upgrade=argument.upgradepython, upgrade_deps=argument.upgradepip, prompt=argument.prompt)
					
					print_log(lang(["Création du dossier de l'environnement","Create environment directory"]))
					virtual.ensure_directories(virtdir)
					if not os.path.exists(context.inc_path) or not os.path.exists(context.bin_path) or not os.path.exists(context.lib_path):
						print_log(lang(["ERREUR: Le dossier de l'environnement n'a pas été créé","ERROR: Environent directory not created"]))
						sys.exit()
					
					print_log(lang(["Création du fichier de config","Create configuration file"]))
					virtual.create_configuration(context)
					if not os.path.exists(context.cfg_path):
						print_log(lang(["ERREUR: Le fichier de config n'a pas été créé","ERROR: Configuration file not created"]))
						sys.exit()
					
					print_log(lang(["Copie de l'exécutable Python","Copy python executable"]))
					virtual.setup_python(context)
					if not os.path.exists(context.env_exe):
						print_log(lang(["ERREUR: L'exécutable n'a pas été copié","ERROR: Python executable not copied"]))
						sys.exit()
					
					print_log(lang(["Création des scripts d'activation","Create activation script"]))
					virtual.setup_scripts(context)
					if not os.path.exists(context.bin_path+path_rep[0]+"activate"):
						print_log(lang(["ERREUR: Les scripts d'activation n'ont pas été créé","ERROR: Activation script not created"]))
						sys.exit()

					if not argument.nopip:
						print_log(lang(["Installation de pip","Install pip"]))
						virtual._setup_pip(context)
						if os.name=='nt':
							pipname = 'pip.exe'
						else:
							pipname = 'pip'

						if not os.path.exists(context.bin_path+path_rep[0]+pipname):
							print_log(lang(["ERREUR: Pip n'a pas été installé","ERROR: Pip not installed"]))
							sys.exit()

						if argument.upgradepip:
							print_log(lang(["Recherche de mise à jour","Check update"]))
							upgrade_module(context.env_exe,"pip", argument.proxy)
							upgrade_module(context.env_exe,"setuptools", argument.proxy)


						if argument.installmodule!=None:
							for package in argument.installmodule.split(","):
								print_log(lang([f"Installation du module {package}",f"Install module {package}"]))
								install_module(context.env_exe,package, argument.proxy)
						
						if argument.requirement!=None:
							if os.path.exists(argument.requirement):
								with open(argument.requirement, 'r') as file:
									for package in file.readlines():
										package = package.rstrip()
										if len(package)!=0:
											print_log(lang([f"Installation du module {package}",f"Install module {package}"]))
											install_module(context.env_exe,package, argument.proxy)

					print_log(lang(["Environnement créé","Environment created"]))

					print_log(lang(["Ajout dans le fichier de config","Add in config file"]))
					venv_data = {}
					venv_data['env_dir'] = context.env_dir 
					venv_data['env_name'] = context.env_name 
					venv_data['env_exe'] = context.env_exe
					venv_data['bin_path'] = context.bin_path
					c = Config(context.cfg_path)
					data = c.load(val='version', section='',default="N.A")
					venv_data['version'] = data
					if argument.tag!=None:
						venv_data['tag'] = argument.tag

					if argument.comment!=None:
						venv_data['comment'] = argument.comment
					
					if argument.projectfolder!=None:
						venv_data['projectfolder'] = path_reg(argument.projectfolder)

					add_venv(venv_data)
				
				elif envc!=None:
					print_log(lang([f"L'environnement {context.env_name} est déjà présent dans le fichier de config",f"Environment {context.env_name} already present in the config file"]))
		
		elif argument.migrate:
			if len(parameter)==0:
				paramenv = os.path.abspath('.')
			else:
				paramenv = path_reg(parameter[0])

			if os.path.exists(paramenv):
				print_log(lang(["Analyse de la structure du dossier","Folder structure analysis"]))
				if not os.path.exists(paramenv+path_rep[0]+"Lib"+path_rep[0]+"site-packages"):
					print_log(lang(["Le dossier site-package n'existe pas","site-package folder doesn't exist"]))
					return

				if (os.name=='nt' and not os.path.exists(paramenv+path_rep[0]+"Scripts"+path_rep[0]+"python.exe")) or (os.name!='nt' and not os.path.exists(paramenv+path_rep[0]+"Scripts"+path_rep[0]+"python")):
					print_log(lang(["L'exécutable Python n'existe pas","Python executable doesn't exist"]))
					return

				if (os.name=='nt' and (not os.path.exists(paramenv+path_rep[0]+"Scripts"+path_rep[0]+"activate.bat") or not os.path.exists(paramenv+path_rep[0]+"Scripts"+path_rep[0]+"activate.ps1"))) or (os.name!='nt' and not os.path.exists(paramenv+path_rep[0]+"Scripts"+path_rep[0]+"activate")):
					print_log(lang(["Le script d'activation n'existe pas","Activate script doesn't exist"]))
					return

				if not os.path.exists(paramenv+path_rep[0]+"pyvenv.cfg"):
					print_log(lang(["Le fichier de config de l'environnement n'existe pas","Config file environment doesn't exist"]))
					return

				print_log(lang(["Environnement valide","Valid environment"]))
				print_log(lang(["Ajout dans le fichier de config","Add in config file"]))
				venv_data = {}
				venv_data['env_dir'] = paramenv

				if argument.name!= None:
					venv_data['env_name'] = argument.name
				else:
					name = paramenv.split(path_rep[0])
					venv_data['env_name'] = name[len(name)-1]

				if load_venv(venv_data['env_name'])!=False:
					print_log(lang([f"L'environnement {venv_data['env_name']} est déjà présent dans le fichier de config",f"Environment {venv_data['env_name']} already present in the config file"]))
					return

				if os.name=='nt':
					venv_data['env_exe'] = paramenv+path_rep[0]+"Scripts"+path_rep[0]+"python.exe"
				else:
					venv_data['env_exe'] = paramenv+path_rep[0]+"Scripts"+path_rep[0]+"python"
				venv_data['bin_path'] = paramenv+path_rep[0]+"Scripts"
				c = Config(paramenv+path_rep[0]+"pyvenv.cfg")
				data = c.load(val='version', section='',default="N.A")
				if data=="N.A":
					data = c.load(val='version_info', section='',default="N.A")
				venv_data['version'] = data
				
				if argument.tag!=None:
					venv_data['tag'] = argument.tag

				if argument.comment!=None:
					venv_data['comment'] = argument.comment
				
				if argument.projectfolder!=None:
					venv_data['projectfolder'] = path_reg(argument.projectfolder)

				add_venv(venv_data)
			else:
				print_log(lang(["Le dossier n'existe pas","Folder doesn't exist"]))

		elif argument.open:
			envc = load_venv(parameter[0])
			if envc!=False and envc!=None:
				if os.path.exists(envc['bin_path']) and os.path.isdir(envc['bin_path']):
					if argument.shell:
						cmd = envc['env_exe']
					else:
						OSType = get_os()
						if OSType=='cmd':
							activate_file='activate.bat'
							if os.path.exists(envc['bin_path']+path_rep[0]+activate_file):
								cmd = ['cmd', '/k']
								target = ""
								### Add alias CMD
								if 'projectfolder' in envc:
									target+=f"doskey cdproject=cd {envc['projectfolder']} & "
								else:
									target+=f"doskey cdproject=echo "+lang(["Le dossier de projet n'est pas configuré","Project Folder not configure"])+" & "
								target+=f"doskey cdenv=cd {envc['env_dir']} & "
								target+=f"doskey shellenv={envc['env_exe']} & "
								target+=f"doskey zpenv={sys.executable} -m zpenv $* & "
								target+=f'doskey help=echo "'+lang(["cdenv      se déplacer dans le dossier de l\'environnement`ncdproject  se déplacer dans le dossier du projet`nshellenv   accéder au shell python`nzpenv      accéder à zpenv","cdenv      move to environment folder`ncdproject  move to project folder`nshellenv   access python shell`nzpenv      access zpenv"])+'" & '
								### END Add alias
								target+="pushd "+envc['bin_path']+" & "+activate_file+" & popd"
								cmd.append(target)
							else:
								print_log(lang(["ERREUR: Le script d'activation n'existe pas","ERROR: Activate script not exist"]))
								sys.exit()

						elif OSType=='powershell.exe' or os.name=='nt':
							activate_file='activate.ps1'
							if os.path.exists(envc['bin_path']+path_rep[0]+activate_file):
								cmd = ['powershell', '-NoExit', '-Command']
								target = ""
								### Add alias PS1
								if 'projectfolder' in envc:
									target+='function cdproject{cd "'+envc['projectfolder']+'"}; '
								else:
									target+='function cdproject{Write-Host '+lang(["Le dossier de projet n'est pas configuré","Project Folder not configure"])+'}; '
								target+='function cdenv{cd "'+envc['env_dir']+'"}; '
								target+='function shellenv{'+envc['env_exe']+'}; '
								target+='function zpenv{'+sys.executable+' -m zpenv}; '
								target+='function help{Write-Host "'+lang(["cdenv      se déplacer dans le dossier de l\'environnement`ncdproject  se déplacer dans le dossier du projet`nshellenv   accéder au shell python`nzpenv      accéder à zpenv","cdenv      move to environment folder`ncdproject  move to project folder`nshellenv   access python shell`nzpenv      access zpenv"])+'"}; '
								### END Add alias
								target+='. "'+envc['bin_path']+path_rep[0]+activate_file+'"'
								cmd.append(target)
							else:
								print_log(lang(["ERREUR: Le script d'activation n'existe pas","ERROR: Activate script not exist"]))
								sys.exit()
						
						else:
							activate_file='activate'
							if os.path.exists(envc['bin_path']+path_rep[0]+activate_file):
								cmd = []
								target = ""
								### Add alias Linux
								if 'projectfolder' in envc:
									target+=f"alias cdproject=\'cd {envc['projectfolder']}\' && "
								else:
									target+="alias cdproject=\'echo "+lang(["Le dossier de projet n'est pas configuré","Project Folder not configure"])+"\' && "
								target+=f"alias cdenv='cd {envc['env_dir']}' && "
								target+=f"alias shellenv='{envc['env_exe']}' && "
								target+=f"alias zpenv='{sys.executable} -m zpenv $*' && "
								target+=f'alias help=\'echo -e "'+lang(["cdenv      se déplacer dans le dossier de l\'environnement\ncdproject  se déplacer dans le dossier du projet\nshellenv   accéder au shell python\nzpenv      accéder à zpenv","cdenv      move to environment folder\ncdproject  move to project folder\nshellenv   access python shell\nzpenv      access zpenv"])+'"\' && '
								### END alias Linux
								target+="source "+envc['bin_path']+path_rep[0]+activate_file
								cmd.append(target)
							else:
								print_log(lang(["ERREUR: Le script d'activation n'existe pas","ERROR: Activate script not exist"]))
								sys.exit()

					subprocess.call(cmd, shell=True)
				else:
					print_log(lang(["ERREUR: Dossier d'environnement introuvable","ERROR: Environment folder not found"]))
			
		elif argument.list:
			if os.path.exists(argument.configfile):
				with open(argument.configfile, 'r') as file:
					content = file.read()
					try:
						content = json.loads(content)
						for envname in content:
							print(f" - {envname}")
					except:
						print_log(lang(["ERREUR: Fichier de config corrompu","ERROR: Config file corrupted"]))

		elif argument.info:
			for paramenv in parameter[0].split(","):
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					print(f"Environment name:        {envc['env_name']}")  
					print(f"Environment path:        {envc['env_dir']}")  
					print(f"Environment version:     {envc['version']}")
					if "tag" in envc: 
						print(f"Environment tag:         {envc['tag']}") 
					if "comment" in envc and envc['comment']!="": 
						print(f"Environment commentaire: {envc['comment']}")
					if "projectfolder" in envc: 
						print(f"Project Folder:          {envc['projectfolder']}\n")

		elif argument.installmodule!=None:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					for package in argument.installmodule.split(","):
						print_log(lang([f"Installation du module {package}",f"Install module {package}"]))
						install_module(envc['env_exe'],package, argument.proxy)
			
		elif argument.removemodule!=None:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					for package in argument.removemodule.split(","):
						print_log(lang([f"Suppression du module {package}",f"Remove module {package}"]))
						remove_module(envc['env_exe'],package)

		elif argument.requirement!=None:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					if os.path.exists(argument.requirement):
						with open(argument.requirement, 'r') as file:
							for package in file.readlines():
								package = package.rstrip()
								if len(package)!=0:
									print_log(lang([f"Installation du module {package}",f"Install module {package}"]))
									install_module(envc['env_exe'],package, argument.proxy)
		
		elif argument.upgrademodule!=None:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					for package in argument.upgrademodule.split(","):
						print_log(lang([f"Mise à jour du module {package}",f"Upgrade module {package}"]))
						upgrade_module(envc['env_exe'],package, argument.proxy)

		elif argument.remove:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					print_log(lang(["Suppression de l'environnement","Remove environment"]))
					purgedir=True
					if not argument.nopurge:
						if os.path.exists(envc['env_dir']):
							print_log(lang(["Suppresion d'un dossier d'environnement","Remove environment folder"]))
							try:
								shutil.rmtree(envc['env_dir'])
							except PermissionError:
								print_log(lang(["ERREUR: Autorisation refusée pour supprimer le dossier d'environnement","ERROR: Permission Denied to remove environment folder"]))
								purgedir=False
							except Exception as err:
								print_log(f"Error: {err}")
								purgedir=False
						else:
							print_log(lang(["Le dossier d'environnement n'existe pas","Environment folder not exist"]))
					if purgedir:
						del_venv(envc['env_name'])

		elif argument.upgradepython:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				virtual = venv.EnvBuilder(upgrade=argument.upgradepython)
				virtdir = path_reg(paramenv)
				context = Context(virtdir, argument.name)
				print_log(lang(["Mise à jour de Python","Update Python"]))
				try:
					virtual.setup_python(context)
					print_log(lang(["Python mis à jour","Python updated"]))

					c = Config(context.cfg_path)
					data = c.load(val='version', section='',default="N.A")
					if data=="N.A":
						data = c.load(val='version_info', section='',default="N.A")
					edit_venv(context.env_name,"version",data)

				except Exception as err:
					print_log(lang([f"Erreur mise à jour Python: {setup_python}",f"Error python update: {setup_python}"]))

		elif argument.projectfolder or argument.tag or argument.comment:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					if argument.tag!=None:
						edit_venv(paramenv,"tag",envc['tag']+","+argument.tag)
					if argument.comment!=None:
						edit_venv(paramenv,"comment",argument.comment)
					if argument.projectfolder!=None:
						folder = path_reg(argument.projectfolder)
						if os.path.exists(folder) and os.path.isdir(folder):
							edit_venv(paramenv,"projectfolder",folder)
						else:
							print_log(lang(["Dossier de projet non valide","Project folder not valid"]))
				if envc==False:
					print_log(lang([f"L'environnement {paramenv} n'existe pas", f"Environment {paramenv} doesn't exist"]))

		elif argument.removecomment:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					edit_venv(paramenv,"comment","")

				if envc==False:
					print_log(lang([f"L'environnement {paramenv} n'existe pas", f"Environment {paramenv} doesn't exist"]))

		elif argument.removetag:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					tag = envc['tag'].split(",")
					tag.remove(argument.removetag)
					edit_venv(paramenv,"tag",",".join(tag))
				if envc==False:
					print_log(lang([f"L'environnement {paramenv} n'existe pas", f"Environment {paramenv} doesn't exist"]))
		
		elif argument.installpip:
			for paramenv in parameter[0].split(","):
				print_log(lang([f"Environnement {paramenv}", f"Environment {paramenv}"]))
				envc = load_venv(paramenv)
				if envc!=False and envc!=None:
					print_log(lang([f"Installation de pip", f"Install pip"]))
					cmd = [envc['env_exe'], '-m', 'ensurepip']
					if argument.proxy!=None:
						cmd.append('--proxy='+argument.proxy)
					proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					stdout, stderr = proc.communicate()
					if len(stdout)!=0:
						print_log(lang([f"Pip installé",f"Pip installed"]))
					else:
						print_log(lang([f"ERREUR: Pip non installé\nMessage d'erreur: {stderr.decode()}",f"ERROR: Pip not installed\nError message: {stderr.decode()}"]))
