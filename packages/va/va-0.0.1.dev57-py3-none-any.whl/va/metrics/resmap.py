import subprocess
import sys
import os
from distutils.spawn import find_executable
import numpy as np
import mrcfile
from PIL import Image, ImageSequence
import json
import codecs

def create_folder(output_path):
    """
        create output folder inside va directory

    :return: model related path of folder
    """

    fullname = '{}'.format(output_path)

    if not os.path.isdir(fullname):
        os.mkdir(fullname, mode=0o777)
    else:
        print('{} is exist'.format(fullname))



def run_resmap(mapone, maptwo, output_path):
    errlist = []
    try:
        assert find_executable('ResMap-1.90-MacOSX') is not None
        respath = find_executable('ResMap-1.90-MacOSX')
        create_folder(output_path)
        resmap_cmd = '{} {} {} --noguiSplit --noiseDiag --doBenchMarking'.format(respath, mapone, maptwo)
        print(resmap_cmd)
        try:
            process = subprocess.Popen(resmap_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       cwd=output_path)
            output = process.communicate('n\n')[0]
            errqscore = 'error'
            if sys.version_info[0] >= 3:
                for item in output.decode('utf-8').split('\n'):
                    # item = cline.decode('utf-8').strip()
                    print(item)
                    if errqscore in item.lower():
                        errline = item.strip()
                        errlist.append(errline)
                        assert errqscore not in output.decode('utf-8'), errline

            else:
                for item in output.split('\n'):
                    print(item)
                    if errqscore in item.lower():
                        errline = item.strip()
                        errlist.append(errline)
                        assert errqscore not in output.decode('utf-8'), errline
        except subprocess.CalledProcessError as suberr:
            err = 'Local resolution from ResMap calculation error: {}.'.format(suberr)
            errlist.append(err)
            sys.stderr.write(err + '\n')
    except AssertionError as exerr:
        err = 'ResMap executable is not there.'
        errlist.append(err)
        sys.stderr.write('ResMap executable is not there: {}\n'.format(exerr))

    return errlist

def resmap_filecheck(mapone, output_path):
    """
        Check if all output from ResMap are ready
    :return: True(all file exist) or False (not all file exist
    """

    output_path = output_path
    mapname = os.path.basename(mapone)
    mapfile = '{}{}_ori.map'.format(output_path, os.path.splitext(mapname)[0])
    resmapname = '{}{}_ori_resmap.map'.format(output_path, os.path.splitext(mapname)[0])
    resmap_chimera = '{}{}_ori_resmap_chimera.cmd'.format(output_path, os.path.splitext(mapname)[0])
    check = os.path.isfile(mapfile) and os.path.isfile(resmapname) and os.path.isfile(resmap_chimera)

    return check if check else False


def resmap_chimerax(mapone, output_path):
    """
        Generate chimerax cmd for ResMap results
    :return:
    """

    mapname = os.path.basename(mapone)
    output_chimerax_file = '{}{}_chimerax.cxc'.format(output_path, os.path.basename(mapone))
    orgmap = '{}{}_ori.map'.format(output_path, os.path.splitext(mapname)[0])
    resmap = '{}{}_ori_resmap.map'.format(output_path, os.path.splitext(mapname)[0])
    header = mrcfile.open(mapone, mode='r', header_only=True)
    voxsizes = header.voxel_size.tolist()
    if all(element == voxsizes[0] for element in voxsizes):
        voxsize = voxsizes[0]
        mmin = round((2.2 * voxsize) / 0.1) * 0.1  # round to the nearest 0.1
        mmax = round((4.0 * voxsize) / 0.5) * 0.5  # round to the nearest 0.5
    else:
        voxsizemin = voxsizes.min()
        voxsizemax = voxsizes.max()
        mmin = round((2.2 * voxsizemin) / 0.1) * 0.1  # round to the nearest 0.1
        mmax = round((4.0 * voxsizemax) / 0.5) * 0.5  # round to the nearest 0.5
        print('Voxel sizes are not the same!!!')

    n = header.header.nx
    colors_chimerax = ['blue', 'cyan', 'green', 'yellow', 'orange', 'red']
    values_chimerax = np.linspace(mmin, mmax, len(colors_chimerax))
    colorstr = ''
    for i in range(len(colors_chimerax)):
        colorstr += '%.2f' % values_chimerax[i] + ',' + colors_chimerax[i] + ':'
    colorstr += '%.2f' % (values_chimerax[i] + 0.01) + ',' + 'gray'
    with open(output_chimerax_file, 'w') as fp:
        fp.write("windowsize 800 800\n")
        fp.write("set bg_color white\n")
        fp.write("open " + orgmap + " format ccp4" + '\n')
        fp.write("open " + resmap + " format ccp4" + '\n')
        fp.write("volume #2 hide\n")
        fp.write("color sample #1 map #2 palette " + colorstr + '\n')
        fp.write("volume #1 planes z,0 step 1 level -1 style surface\n")
        fp.write("camera ortho\n")
        fp.write("zoom 1.3\n")
        fp.write("view cofr True\n")
        # fp.write("camera ortho\n")
        fp.write('2dlabels text "0" xpos 0.8 ypos 0.1\n')
        # fp.write("vop gaussian #1 sDev 5 model #3")
        # fp.write("volume #3 level 0.02 step 1 color rgba(0%, 80%, 40%, 0.5)")
        # fp.write("volume #3 level 0.02 step 1 color 60,0,80,50")
        # fp.write("zoom 0.5")
        fp.write("movie record size 800,800\n")
        # fp.write('perframe "volume #1 plane z,$1" range 198,0')
        fp.write('perframe "volume #1 plane z,$1 ; 2dlabel #3.1 text $1" range 0,{},2\n'.format(n))
        fp.write("wait {}\n".format(str(round(n/2) + 2)))
        fp.write("movie encode {}_zplanes.png quality high\n\n\n\n".format(resmap))

        # X
        fp.write("close session\n")
        fp.write("set bg_color white\n")
        fp.write("open " + orgmap + " format ccp4" + '\n')
        fp.write("open " + resmap + " format ccp4" + '\n')
        fp.write("volume #2 hide\n")
        fp.write("color sample #1 map #2 palette " + colorstr + '\n')
        fp.write("turn -x 90\n")
        fp.write("turn -y 90\n")
        fp.write("volume #1 planes x,0 step 1 level -1 style surface\n")
        fp.write("camera ortho\n")
        fp.write("zoom 1.3\n")
        fp.write("view cofr True\n")
        # fp.write("view orient\n")
        # fp.write("camera ortho\n")
        fp.write('2dlabels text "0" xpos 0.8 ypos 0.1\n')
        # fp.write("vop gaussian #1 sDev 5 model #3")
        # fp.write("volume #3 level 0.02 step 1 color rgba(0%, 80%, 40%, 0.5)")
        # fp.write("volume #3 level 0.02 step 1 color 60,0,80,50")
        # fp.write("zoom 0.5")
        fp.write("movie record size 800,800\n")
        # fp.write('perframe "volume #1 plane z,$1" range 198,0')
        fp.write('perframe "volume #1 plane x,$1 ; 2dlabel #3.1 text $1" range 0,{},2\n'.format(n))
        fp.write("wait {}\n".format(str(round(n/2) + 2)))
        fp.write("movie encode {}_xplanes.png quality high\n".format(resmap))

        # Y
        fp.write("close session\n")
        fp.write("set bg_color white\n")
        fp.write("open " + orgmap + " format ccp4" + '\n')
        fp.write("open " + resmap + " format ccp4" + '\n')
        fp.write("volume #2 hide\n")
        fp.write("color sample #1 map #2 palette " + colorstr + '\n')
        fp.write("turn x 90\n")
        fp.write("turn z 90\n")
        fp.write("volume #1 planes y,0 step 1 level -1 style surface\n")
        fp.write("camera ortho\n")
        fp.write("zoom 1.3\n")
        fp.write("view cofr True\n")
        # fp.write("view orient\n")
        # fp.write("camera ortho\n")
        fp.write('2dlabels text "0" xpos 0.7 ypos 0.1\n')
        # fp.write("vop gaussian #1 sDev 5 model #3")
        # fp.write("volume #3 level 0.02 step 1 color rgba(0%, 80%, 40%, 0.5)")
        # fp.write("volume #3 level 0.02 step 1 color 60,0,80,50")
        # fp.write("zoom 0.5")
        fp.write("movie record size 800,800\n")
        # fp.write('perframe "volume #1 plane z,$1" range 198,0')
        fp.write('perframe "volume #1 plane y,$1 ; 2dlabel #3.1 text $1" range 0,{},2\n'.format(n))
        fp.write("wait {}\n".format(str(round(n/2) + 2)))
        fp.write("movie encode {}_yplanes.png quality high\n".format(resmap))
        fp.write('close all\n')
        fp.write('exit')
        fp.close()

        return output_chimerax_file

def run_resmap_chimerax(bindisplay, locCHIMERA, cxcfile):
    """

    :return:
    """
    errlist = []
    try:
        if not bindisplay:
            subprocess.check_call(locCHIMERA + " --offscreen --nogui " + cxcfile, cwd=os.path.dirname(cxcfile),
                                  shell=True)
            print('Animated PNG for ResMap result has been produced.')
        else:
            subprocess.check_call(locCHIMERA + " " + cxcfile, cwd=os.path.dirname(cxcfile), shell=True)
            print('Animated PNG for ResMap result has been produced.')
    except subprocess.CalledProcessError as suberr:
        err = 'Saving ResMap local resolution animated png error: {}.'.format(suberr)
        errlist.append(err)
        sys.stderr.write(err + '\n')

    return errlist

def save_imagestojson(resmapname, output_filename):
    """

    :return:
    """
    basename = os.path.basename(resmapname)
    x_local = '{}_xplanes.png'.format(resmapname)
    y_local = '{}_yplanes.png'.format(resmapname)
    z_local = '{}_zplanes.png'.format(resmapname)
    org_xyz_pngs = os.path.isfile(x_local) and os.path.isfile(y_local) and os.path.isfile(z_local)
    org_xyz_pngs_scaled = False
    if org_xyz_pngs:
        x_local_scaled = '{}_scaled_xplanes.png'.format(resmapname)
        y_local_scaled = '{}_scaled_yplanes.png'.format(resmapname)
        z_local_scaled = '{}_scaled_zplanes.png'.format(resmapname)
        size = (300,300)
        resize_apng(x_local, x_local_scaled, size)
        resize_apng(y_local, y_local_scaled, size)
        resize_apng(z_local, z_local_scaled, size)
        org_xyz_pngs_scaled = os.path.isfile(x_local_scaled) and os.path.isfile(y_local_scaled) and \
                              os.path.isfile(z_local_scaled)

    if org_xyz_pngs and org_xyz_pngs_scaled:
        result_dict = {'local_resolution': {'ResMap': {'original': {'x': os.path.basename(x_local),
                                                                    'y': os.path.basename(y_local),
                                                                    'z': os.path.basename(z_local)}},
                                                        'scaled': {'x': os.path.basename(x_local_scaled),
                                                                   'y': os.path.basename(y_local_scaled),
                                                                   'z': os.path.basename(z_local_scaled)}}}
        try:
            with codecs.open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f)
        except:
            sys.stderr.write(
                'Saving ResMap view to JSON error: {}.\n'.format(sys.exc_info()[1]))
    else:
        print('Missing ResMap result images.')



def resize_apng(input_file, output_file, size):
    # Open the APNG file
    input_apng = Image.open(input_file)

    # Create a list to store resized frames
    resized_frames = []

    # Iterate over each frame of the APNG
    for frame in ImageSequence.Iterator(input_apng):
        # Resize the frame's image
        resized_image = frame.copy().resize(size, Image.ANTIALIAS)
        resized_frames.append(resized_image)

    # Save the resized frames as an APNG
    resized_frames[0].save(output_file, save_all=True, append_images=resized_frames[1:], optimize=False, duration=input_apng.info.get('duration', 100), loop=input_apng.info.get('loop', 0))

# Usage example:








