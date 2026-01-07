#!/usr/bin/env python3
import subprocess
import argparse
import os
from pathlib import Path
from datetime import datetime
import sys

class Enumerator:
    def __init__(self, target, mode):
        self.target = target
        self.mode = mode
        self.output_dir = Path.home() / target
        self.setup_output_dir()
    
    def setup_output_dir(self):
        """Create output directory if it doesn't exist"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] Output directory: {self.output_dir}")
    
    def run_command(self, cmd, output_file):
        """Execute command and save output"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"{timestamp}_{output_file}"
        
        print(f"\n[+] Running: {' '.join(cmd)}")
        print(f"[*] Saving to: {output_path}")
        
        try:
            with open(output_path, 'w') as f:
                # Write command as header
                f.write(f"# Command: {' '.join(cmd)}\n")
                f.write(f"# Timestamp: {timestamp}\n")
                f.write(f"# Target: {self.target}\n")
                f.write("#" + "="*70 + "\n\n")
                
                # Run command
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                
                # Stream output to both terminal and file
                for line in process.stdout:
                    print(line, end='')
                    f.write(line)
                
                process.wait()
                
            if process.returncode == 0:
                print(f"[✓] Completed successfully")
            else:
                print(f"[!] Command exited with code {process.returncode}")
                
        except Exception as e:
            print(f"[✗] Error running command: {e}")
            return False
        
        return True
    
    def nmap_ctf(self):
        """Nmap scan optimized for CTF environments"""
        cmd = ['nmap', '-sC', '-sV', '-Pn', '-T4', self.target]
        self.run_command(cmd, 'nmap_ctf.txt')
    
    def nmap_realworld(self):
        """Nmap scan for real-world pentesting"""
        cmd = ['nmap', '-sV', '-Pn', '--open', '-p-', self.target]
        self.run_command(cmd, 'nmap_full.txt')
    
    def run_enumeration(self):
        """Execute enumeration based on mode"""
        print(f"\n{'='*70}")
        print(f"Smart Enumerator - {self.mode.upper()} Mode")
        print(f"Target: {self.target}")
        print(f"{'='*70}")
        
        if self.mode == 'ctf':
            self.nmap_ctf()
        elif self.mode == 'real':
            self.nmap_realworld()
        
        print(f"\n{'='*70}")
        print(f"[✓] Enumeration complete!")
        print(f"[*] Results saved in: {self.output_dir}")
        print(f"{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Smart Enumeration Tool for Pentesting and CTFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t 10.10.10.1 -m ctf       # CTF quick scan
  %(prog)s -t 10.10.10.1 -m real      # Full port scan for real engagements
        """
    )
    
    parser.add_argument('-t', '--target', required=True,
                       help='Target IP address or hostname')
    parser.add_argument('-m', '--mode', required=True,
                       choices=['ctf', 'real'],
                       help='Enumeration mode: ctf (fast) or real (comprehensive)')
    
    args = parser.parse_args()
    
    # Check if nmap is installed
    try:
        subprocess.run(['nmap', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[✗] Error: nmap is not installed or not in PATH")
        sys.exit(1)
    
    enum = Enumerator(args.target, args.mode)
    enum.run_enumeration()

if __name__ == '__main__':
    main()
