import json, os, os.path, argparse, glob

parser = argparse.ArgumentParser(description='Generate JSON configuration file for SystemDataScope')
parser.add_argument('root_dir', type=str,
                    help='Root directory with collectd RRD databases, for example /tmp/collectd/Jolla')

args = parser.parse_args()

Root = args.root_dir
os.chdir(Root)

Config = {}

Config["variables"] = {
	"COLOR_LINE_1": "#0000FF"
    }

Config["page"] = {
    
    "title": "Overview",
    "plots": [
        { "type": "CPU/overview",
	  
          "subplots": {
	      "title": "Details $COLOR_LINE_1$",
	      "plots": [
                  { "type": "CPU/system" }
	      ]
          }
        },
	
        { "type": "CPU/user" }
    ]
}

class Stack:
    def __init__(self, t = "LINE"):
        self.count = 0
        self.lines = []
        self.gt = t

    def add(self, l, makeLine=False):
        cmd = self.gt + ":" + l
        if self.count > 0 and not makeLine:
            cmd += ":STACK"
        self.lines.append(cmd)
        self.count += 1

    def str(self):
        s = ""
        for i in self.lines: s += i + " "
        return s    
        

Config["types"] = {}

# CPU overview
command_def = "-t \"CPU usage overview\" --upper-limit 100 --lower-limit 0 --rigid "
command_line = ""
files = []
s = Stack()
for g in glob.glob( "cpu/*.rrd" ):
    if g.find("freq") < 0:
        hack = g[12:-4]
        command_def += "DEF:" + hack + "=" + g + ":value:AVERAGE "
        # command_line += "LINE:" + hack + "$COLOR_LINE_1$:\"" + hack + "\\l\"" + " "
        s.add( hack + "$COLOR_LINE_1$:\"" + hack + "\\l\"" )
        files.append(g)

command_line = s.str()

Config["types"]["CPU/overview"] = { "command": command_def + command_line,
                                 "files": files }

print json.dumps(Config, indent=3)
