#
# Helper script to convert COLMAP binary models to PLY or TXT
#

import os
import logging
from argparse import ArgumentParser

parser = ArgumentParser("Colmap model converter")
parser.add_argument("--source_path", "-s", required=True, type=str, help="Path to the dataset root (containing sparse/0/)")
parser.add_argument("--ply", action='store_true', help="Convert to PLY format for visualization")
parser.add_argument("--txt", action='store_true', help="Convert to TXT format for debugging")
parser.add_argument("--colmap_executable", default="", type=str)
args = parser.parse_args()

colmap_command = '"{}"'.format(args.colmap_executable) if len(args.colmap_executable) > 0 else "colmap"

# Standard Gaussian Splatting path structure
input_model_path = os.path.join(args.source_path, "sparse", "0")

if not os.path.exists(input_model_path):
    logging.error(f"Input model path {input_model_path} does not exist. Please run convert.py first.")
    exit(1)

if not args.ply and not args.txt:
    print("No conversion format specified. Please use --ply or --txt.")
    exit(0)

if args.ply:
    print("Converting to PLY...")
    # PLY output requires a specific file path
    output_ply_path = os.path.join(input_model_path, "points3D.ply")
    
    ply_cmd = (colmap_command + " model_converter " +
               "--input_path " + input_model_path + " " +
               "--output_path " + output_ply_path + " " +
               "--output_type PLY")
    
    exit_code = os.system(ply_cmd)
    if exit_code != 0:
        logging.error(f"PLY conversion failed with code {exit_code}.")
    else:
        print(f"PLY saved to {output_ply_path}")

if args.txt:
    print("Converting to TXT...")
    # TXT output requires a directory path (it will create cameras.txt, images.txt, points3D.txt)
    # We output to the same directory.
    
    txt_cmd = (colmap_command + " model_converter " +
               "--input_path " + input_model_path + " " +
               "--output_path " + input_model_path + " " +
               "--output_type TXT")
    
    exit_code = os.system(txt_cmd)
    if exit_code != 0:
        logging.error(f"TXT conversion failed with code {exit_code}.")
    else:
        print(f"TXT files (cameras.txt, images.txt, points3D.txt) saved to {input_model_path}")

print("Done.")
