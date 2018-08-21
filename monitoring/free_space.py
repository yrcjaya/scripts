import subprocess
import json


def free_space(block_size=1024):
    output = subprocess.check_output(['df', '--block-size=%d'%block_size])
    lines = output.split('\n')
    lines = lines[1:-1] # Remove header and last blank line
    filesystems = []
    for line in lines:
        cols = line.split()
        if not cols[0].startswith('/dev'):
            continue
        fs = {
            'dev': cols[0],
            'size': int(cols[1])*block_size,
            'used': int(cols[2])*block_size,
            'free': int(cols[3])*block_size,
            'used_pct': cols[4],
            'mount_point': cols[5]
        }
        filesystems.append(fs)
    return filesystems


def output_json(space):
    return json.dumps(space, indent=4)

def output_prometheus(space):
    output=''
    for fs in space:
        output += 'disk_size{dev="%s", mount_point="%s"} %s\n' % (fs['dev'], fs['mount_point'], fs['size'])
        output += 'disk_used{dev="%s", mount_point="%s"} %s\n' % (fs['dev'], fs['mount_point'], fs['used'])
        output += 'disk_free{dev="%s", mount_point="%s"} %s\n' % (fs['dev'], fs['mount_point'], fs['free'])
    return output


if __name__ == '__main__':
    print output_prometheus(free_space())
