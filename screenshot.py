# A simple script to take screenshots and upload them to S3
# Why? Because I lost my old script :(
#
# For now you need to have `scrot` installed, but that's pretty
# much the only requirement.
# Author: staticfox <staticfox@staticfox.net>
import boto3
import pyperclip
import time
import toml
import subprocess
from subprocess import check_call

class S3Shot(object):
    def __init__(self):
        self.bucket = ''
        self.key = ''
        self.location = ''
        self.visibility = ''
        self.want_clipboard = True

    def load_config(self):
        yesses = ['yes', '1', 'true']
        with open('config.toml') as conf:
            config = toml.loads(conf.read())
            self.bucket = config['s3']['bucket_name']
            self.key = config['s3']['path']
            self.visibility = config['s3']['visibility']
            self.location = config['system']['image_storage_path']
            self.want_clipboard = config['system']['want_clipboard'].lower() in yesses

        if self.location[-1] == '/':
            self.location = self.location[:-1]

    def run(self):
        self.load_config()
        file_ts = str(time.time()).replace('.', '-')
        file_name = "{}/{}.png".format(self.location, file_ts)
        bucket = self.bucket
        bucket_url = "https://{}.s3.amazonaws.com/{}/".format(bucket, self.key)

        try:
            pic = check_call(['scrot', file_name, '-s'])
        except subprocess.CalledProcessError as e:
            return print("Failed to take the screenshot: {}".format(e))

        s3 = boto3.resource('s3')
        data = open(file_name, 'rb')
        s3.Bucket(bucket).put_object(
            ACL=self.visibility,
            ContentType='image/png',
            Key="{}/{}.png".format(self.key, file_ts),
            Body=data
        )

        if self.want_clipboard:
            try:
                pyperclip.copy('{}{}.png'.format(bucket_url, file_ts))
            except subprocess.CalledProcessError as e:
                print("Failed to copy: {}".foramt(e))

def run():
    prog = S3Shot()
    prog.run()

if __name__ == '__main__':
    run()
