import re
import sys


DEFINES_FILE_PATH = "Assets/XML/GlobalDefinesVersion.xml"

if __name__ == "__main__":
	args = sys.argv[1:]

	with open(DEFINES_FILE_PATH, "r+") as file:
		file_content = file.read()
		version = re.search(r"<DefineTextVal>(.*)</DefineTextVal>", file_content).group(1)
		
		if "." in version:
			major, minor, subminor = version.split(".")

			new_version = version

			if len(args) > 0 and args[0] == 'major':
				new_version = f"{int(major)+1}.{minor}.{subminor}"
			elif len(args) > 0 and args[0] == 'minor':
				new_version = f"{major}.{int(minor)+1}.{subminor}"
			else:
				new_version = f"{major}.{minor}.{int(subminor)+1}"

			print(f"Updated mod version to {new_version}")
		
			file.seek(0)
			file.write(file_content.replace(version, new_version))
			file.truncate()
		else:
			print("Unexpected format, did not increment")