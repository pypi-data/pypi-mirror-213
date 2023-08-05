"""
lsb - Simple Python package for steganography.
This is the only file in the lsb package.
"""
from numpy import array as _a
from numpy import reshape as _r
from numpy import frombuffer as _f
from numpy import uint8 as _u
from argparse import ArgumentParser as _ap
from PIL import Image as _i
from PIL import ImageTk as _itk
import wave
from numpy import short as _s
from platform import system as _t
from uuid import uuid4 as _8
import os as _os
import des as _d
from base64 import b64encode as _b, b64decode as _bd
from hashlib import md5 as _m
from chardet import detect
import rsa as _rsa
def _4(*args, **kwargs):
    return str(_8(*args, **kwargs))


try:
    import tkinter as _tk
except:
    try:
        import Tkinter as _tk
    except:
        tk_support = False
    else:
        tk_support = True
else:
    tk_support = True
try:
    import pyaudio as _p
except:
    pyaudio_support = False
else:
    pyaudio_support = True
try:
    from tqdm import tqdm
except:
    tqdm_support = False
else:
    tqdm_support = True


def mode_lsb1(x, dec):
    return (
        (
            [
                x >> 7,
                (x >> 6) & 1,
                (x >> 5) & 1,
                (x >> 4) & 1,
                (x >> 3) & 1,
                (x >> 2) & 1,
                (x >> 1) & 1,
                x & 1,
            ],
            1,
        )
        if not dec
        else sum([x[i] << (7 - i) for i in range(8)])
    )


def mode_lsb2(x, dec):
    return (
        ([x >> 6, (x >> 4) & 3, (x >> 2) & 3, x & 3], 2)
        if not dec
        else sum([x[i] << ([6, 4, 2, 0][i]) for i in range(len([6, 4, 2, 0]))])
    )


def mode_lsb3(x, dec):
    return (
        ([x >> 5, (x >> 2) & 7, x & 3], 3)
        if not dec
        else sum([x[i] << ([5, 2, 0][i]) for i in range(len([5, 2, 0]))])
    )


def lsbenc(img, text, mode=mode_lsb1, key=b"",rsakey=None):
    """
    Image steganography encryption
    :param img: Input image (as Numpy array)
    :param text: Text to hide (encoded as bytes)
    :param mode: Mode (lsb1,lsb2,lsb3)
    :param key: DES key (Optional)
    :param rsakey: RSA public key (Optional)
    :return: Image with text hidden
    """
    if key:
        hasher = _m()
        hasher.update(key)
        md5_result = hasher.digest()
        des = _d.DesKey(md5_result)
        text = _b(des.encrypt(text, padding=True))
    if rsakey:
        text=_rsa.encrypt(text,rsakey)
        text= _b(text)
    text += b"\0"
    bit = bytes(img)
    result = b""
    it = 0
    for i in text:
        res = mode(i, False)
        bits = res[1]
        data = res[0]
        for j in range(len(data)):
            result += bytes([((bit[it] >> bits) << bits) | data[j]])
            it += 1
    result += bit[it:]
    resulta = _r(_f(result, dtype=_u), newshape=img.shape)
    return resulta


def lsbdec(img, mode=mode_lsb1, key=b"",rsakey=None):
    """
    Image steganography encryption
    :param img:Input image (as Numpy array)
    :param mode:Mode (lsb1,lsb2,lsb3)
    :param key: DES key (Optional)
    :param rsakey: RSA private key (Optional)
    :return:Text hidden in image (as bytes)
    """
    bits = len(mode(0, False)[0])
    res = b""
    bit = bytes(img)
    it = 0
    while 1:
        l = [f & ((1 << mode(0, False)[-1]) - 1) for f in bit[it : it + bits]]
        if not mode(l, True):
            if rsakey:
                res=_bd(res)
                res=_rsa.decrypt(res,rsakey)
            if key:
                hasher = _m()
                hasher.update(key)
                md5_result = hasher.digest()
                des = _d.DesKey(md5_result)
                res = des.decrypt(_bd(res), padding=True)
            return res
        res += bytes([mode(l, True)])
        it += bits


def lsbenc_audio(audio, text, ofile, framerate=None, mode=mode_lsb1, key=b"",rsakey=None):
    """
    Audio steganography encryption
    :param audio: Input audio (as wave.Wave_read object)
    :param text: Text to hide (encoded as bytes)
    :param ofile: Output file name
    :param framerate:Output file framerate
    :param mode: Mode (lsb1,lsb2,lsb3)
    :param key: DES key (Optional)
    :param rsakey: RSA public key (Optional)
    :return: None
    """
    if key:
        hasher = _m()
        hasher.update(key)
        md5_result = hasher.digest()
        des = _d.DesKey(md5_result)
        text = _b(des.encrypt(text, padding=True))
    if rsakey:
        text=_rsa.encrypt(text,rsakey)
        text= _b(text)
    text += b"\0"
    nf = audio.getnframes()
    ad = audio.readframes(nf)
    bit = list(_f(ad, dtype=_s))
    result = []
    it = 0
    for i in text:
        res = mode(i, False)
        bits = res[1]
        data = res[0]
        for j in range(len(data)):
            result += [((bit[it] >> bits) << bits) | data[j]]
            it += 1
    result += bit[it:]
    resulta = _a(result, dtype=_s)
    if not framerate:
        fr = audio.getframerate() * audio.getnchannels()
    else:
        fr = framerate
    bak = ofile
    if not bak.endswith(".wav"):
        ofile = _os.path.join(_tmp(), _4() + ".wav")
    wf = wave.open(ofile, "wb")
    bt = bytes(resulta)
    wf.setframerate(fr)
    wf.setsampwidth(audio.getsampwidth())
    wf.setnchannels(1)
    wf.writeframes(bt)
    if not bak.endswith(".wav"):
        _os.system('ffmpeg -i "' + ofile + '" "' + bak + '"')


def lsbdec_audio(audio, mode=mode_lsb1, key=b"",rsakey=None):
    """
    Audio steganography decryption
    :param audio:Input audio (as wave.Wave_read object)
    :param mode:Mode (lsb1,lsb2,lsb3)
    :param key: DES key (Optional)
    :param rsakey: RSA private key (Optional)
    :return:Text hidden in audio (as bytes)
    """
    bits = len(mode(0, False)[0])
    res = b""
    nf = audio.getnframes()
    bit = list(_f(audio.readframes(nf), dtype=_s))
    it = 0
    while 1:
        l = [f & ((1 << mode(0, False)[-1]) - 1) for f in bit[it : it + bits]]
        if not mode(l, True):
            if rsakey:
                res=_bd(res)
                res=_rsa.decrypt(res,rsakey)
            if key:
                hasher = _m()
                hasher.update(key)
                md5_result = hasher.digest()
                des = _d.DesKey(md5_result)
                res = des.decrypt(_bd(res), padding=True)
            return res
        res += bytes([mode(l, True)])
        it += bits
    return res


def _tmp():
    if _t() == "Windows":
        return _os.environ["TMP"]
    else:
        return "/tmp"


def _script_image():
    parser = _ap(description="Simple tool for image steganography")
    parser.add_argument("-p", "--operation", help="Operation (e for encrypt，d for decrypt) ")
    parser.add_argument("-t", "--text", help="Text to hide in image")
    parser.add_argument("-e", "--encoding", help="Encoding of text, default is 'ascii'", default="ascii")
    parser.add_argument("-o", "--output", help="Output file name, if the output file name is not configured, the output image will be shown in a Tkinter window")
    parser.add_argument(
        "-m", "--mode", help="mode (lsb1,lsb2,lsb3), default is lsb1", default="lsb1"
    )
    parser.add_argument("-k", "--key", help="DES Key (Optional)", default="")
    parser.add_argument("-a","--auto",help="Automatically detect the encoding of the text in decrypt mode",action='store_true')
    parser.add_argument("-r", "--rsa",
                        help="Use RSA to encrypt the text\nIf in encrypt mode, the program will create pub_(RSA).pem and priv_(RSA).pem\nIf in decrypt mode, the program will read the private key stored (RSA).pem")
    parser.add_argument("image", help="Input image")
    args = parser.parse_args()
    img = _i.open(args.image)
    if args.mode == "lsb1":
        mode = mode_lsb1
    elif args.mode == "lsb2":
        mode = mode_lsb2
    elif args.mode == "lsb3":
        mode = mode_lsb3
    else:
        print("unknown mode: ", args.mode)
        return -1
    if args.operation == "e":
        if args.auto:
            print('--auto should only be used in decrypt mode.')
        if args.text:
            if args.rsa:
                pubkey, privkey = _rsa.newkeys(200)
                with open('pub_' + args.rsa + '.pem', 'wb') as f:
                    f.write(pubkey.save_pkcs1())
                with open('priv_' + args.rsa + '.pem', 'wb') as f:
                    f.write(privkey.save_pkcs1())
            else:
                pubkey = None
            enc = lsbenc(
                _a(img),
                args.text.encode(args.encoding),
                mode=mode,
                key=args.key.encode(args.encoding),
                rsakey=pubkey
            )
            if args.output:
                pilimg = _i.fromarray(enc)
                pilimg.save(args.output)
            else:
                if not tk_support:
                    print("The Python environment does not support Tkinter, so the image cannot be shown")
                    return -1
                else:
                    wn = _tk.Tk()
                    wn.title("Image with text hidden")
                    wn.geometry(f"{enc.shape[0]}x{enc.shape[1]}")
                    pilimg = _i.fromarray(enc)
                    tkimg = _itk.PhotoImage(pilimg)
                    lb = _tk.Label(wn)
                    lb.configure(image=tkimg)
                    lb.place(x=0, y=0, width=enc.shape[0], height=enc.shape[1])
                    wn.mainloop()
        else:
            print("Text to hide is not configured")
            return -1
    elif args.operation == "d":
        if args.text or args.output:
            print("Input text and output file should not be configured in decrypt mode")
            return -1
        else:
            if args.rsa:
                with open(args.rsa + '.pem', 'rb') as f:
                    privkey = _rsa.PrivateKey.load_pkcs1(f.read())
            else:
                privkey = None
            img = _i.open(args.image)
            dec = lsbdec(_a(img), mode=mode, key=args.key.encode(args.encoding),rsakey=privkey)
            if args.auto:
                encoding=detect(dec)['encoding']
                if encoding is None:
                    print('It seems that the encoding is unknown')
                    return -1
            else:
                encoding=args.encoding
            print(dec.decode(encoding))
    else:
        print("unkown operation: ", args.operation)
        return -1


def _script_audio():
    parser = _ap(description="Simple tool for audio steganography")
    parser.add_argument("-p", "--operation", help="Operation (e for encrypt，d for decrypt)")
    parser.add_argument("-t", "--text", help="Text to hide in audio")
    parser.add_argument("-e", "--encoding", help="Encoding of text, default is 'ascii'", default="ascii")
    parser.add_argument("-o", "--output", help="Output file name, if the output file name is not configured, the output audio will be played")
    parser.add_argument(
        "-m", "--mode", help="mode (lsb1,lsb2,lsb3), default is lsb1", default="lsb1"
    )
    parser.add_argument("-f", "--framerate", help="frame rate of output audio")
    parser.add_argument("-b", "--progressbar", help="Display progress bar when playing", action="store_true")
    parser.add_argument("-k", "--key", help="DES Key (Optional)", default="")
    parser.add_argument("-a", "--auto", help="Automatically detect the encoding of the text in decrypt mode",
                        action='store_true')
    parser.add_argument("-r","--rsa",help="Use RSA to encrypt the text\nIf in encrypt mode, the program will create pub_(RSA).pem and priv_(RSA).pem\nIf in decrypt mode, the program will read the private key stored (RSA).pem")
    parser.add_argument("audio", help="Input audio")
    args = parser.parse_args()
    if args.mode == "lsb1":
        mode = mode_lsb1
    elif args.mode == "lsb2":
        mode = mode_lsb2
    elif args.mode == "lsb3":
        mode = mode_lsb3
    else:
        print("unknown mode: ", args.mode)
        return -1
    if args.operation == "e":
        if args.auto:
            print('--auto should only be used in decrypt mode.')
            return -1
        if args.rsa:
            pubkey,privkey=_rsa.newkeys(200)
            with open('pub_'+args.rsa+'.pem','wb') as f:
                f.write(pubkey.save_pkcs1())
            with open('priv_'+args.rsa+'.pem','wb') as f:
                f.write(privkey.save_pkcs1())
        else:
            pubkey=None
        if args.text:
            if args.audio.endswith(".wav"):
                wav = wave.open(args.audio)
            else:
                p = _os.path.join(_tmp(), _4() + ".wav")
                _os.system('ffmpeg -i "' + args.audio + '" "' + p + '"')
                wav = wave.open(p)
            p = str(_4()) + ".wav"
            lsbenc_audio(
                wav,
                args.text.encode(args.encoding),
                _os.path.join(_tmp(), p) if not args.output else args.output,
                framerate=int(args.framerate) if args.framerate else None,
                mode=mode,
                key=args.key.encode(args.encoding),
                rsakey=pubkey
            )
            if not args.output:
                if not pyaudio_support:
                    print("Cannot play the audio because PyAudio is not installed, you can install it via the 'pip install PyAudio' command")
                    return -1
                else:
                    pa = _p.PyAudio()
                    wavfile = wave.open(_os.path.join(_tmp(), p))
                    stream = pa.open(
                        format=pa.get_format_from_width(wavfile.getsampwidth()),
                        channels=wavfile.getnchannels(),
                        rate=wavfile.getframerate(),
                        output=True,
                    )
                    chunk = 1024
                    if args.progressbar:
                        if not tqdm_support:
                            print("Cannot show progress bar because tqdm is not installed, you can install it via the 'pip install tqdm' command")
                            return -1
                        else:
                            tq = tqdm(range(wavfile.getnframes()), unit="frames")
                    while 1:
                        dat = wavfile.readframes(chunk)
                        if not dat:
                            break
                        stream.write(dat)
                        if args.progressbar:
                            tq.update(chunk)
        else:
            print("Text to hide is not configured")
            return -1
    elif args.operation == "d":
        if args.text or args.output or args.progressbar or args.framerate:
            print("Text, output file, progress bar and frame rate should not be configured in decrypt mode")
            return -1
        if args.rsa:
            with open(args.rsa+'.pem','rb') as f:
                privkey=_rsa.PrivateKey.load_pkcs1(f.read())
        else:
            privkey=None
        wav = wave.open(args.audio)
        dec = lsbdec_audio(wav, mode, key=args.key.encode(args.encoding),rsakey=privkey)
        if args.auto:
            encoding=detect(dec)['encoding']
            if encoding is None:
                print('It seems that the encoding is unknown')
                return -1
        else:
            encoding=args.encoding
        print(dec.decode(encoding))
    else:
        print("Unknown operation: ", args.operation)
        return -1


if __name__ == "__main__":
    print("Use the lsb_image command for image steganography, and the lsb_audio command for audio steganography.")
