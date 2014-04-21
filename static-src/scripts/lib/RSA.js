// RSA, a suite of routines for performing RSA public-key computations in
// JavaScript.
//
// Requires BigInt.js and Barrett.js.
//
// Copyright 1998-2005 David Shapiro.
//
// You may use, re-use, abuse, copy, and modify this code to your liking, but
// please keep this header.
//
// Thanks!
// 
// Dave Shapiro
// dave@ohdave.com 

define(['lib/BigInt', 'lib/Barrett'], function(BI, Barrett) {
    BI.setMaxDigits(100);
    function RSAKeyPair(encryptionExponent, decryptionExponent, modulus)
    {
        this.e = BI.biFromHex(encryptionExponent);
        this.d = BI.biFromHex(decryptionExponent);
        this.m = BI.biFromHex(modulus);
        // We can do two bytes per digit, so
        // chunkSize = 2 * (number of digits in modulus - 1).
        // Since biHighIndex returns the high index, not the number of digits, 1 has
        // already been subtracted.
        this.chunkSize = 2 * BI.biHighIndex(this.m);
        this.radix = 16;
        this.barrett = new Barrett(this.m);
        this.encrypt = encryptedString;
        this.decrypt = decryptedString;
    }
    
    function twoDigit(n)
    {
        return (n < 10 ? "0" : "") + String(n);
    }
    
    function encryptedString(s)
        // Altered by Rob Saunders (rob@robsaunders.net). New routine pads the
        // string after it has been converted to an array. This fixes an
        // incompatibility with Flash MX's ActionScript.
    {
        var a = new Array();
        var sl = s.length;
        var i = 0;
        while (i < sl) {
            a[i] = s.charCodeAt(i);
            i++;
        }
    
        while (a.length % this.chunkSize != 0) {
            a[i++] = 0;
        }
    
        var al = a.length;
        var result = "";
        var j, k, block;
        for (i = 0; i < al; i += this.chunkSize) {
            block = new BI.BigInt();
            j = 0;
            for (k = i; k < i + this.chunkSize; ++j) {
                block.digits[j] = a[k++];
                block.digits[j] += a[k++] << 8;
            }
            var crypt = this.barrett.powMod(block, this.e);
            var text = this.radix == 16 ? BI.biToHex(crypt) : BI.biToString(crypt, this.radix);
            result += text + " ";
        }
        return result.substring(0, result.length - 1); // Remove last space.
    }
    
    function decryptedString(s)
    {
        var blocks = s.split(" ");
        var result = "";
        var i, j, block;
        for (i = 0; i < blocks.length; ++i) {
            var bi;
            if (this.radix == 16) {
                bi = BI.biFromHex(blocks[i]);
            }
            else {
                bi = BI.biFromString(blocks[i], this.radix);
            }
            block = this.barrett.powMod(bi, this.d);
            for (j = 0; j <= BI.biHighIndex(block); ++j) {
                result += String.fromCharCode(block.digits[j] & 255,
                                              block.digits[j] >> 8);
            }
        }
        // Remove trailing null, if any.
        if (result.charCodeAt(result.length - 1) == 0) {
            result = result.substring(0, result.length - 1);
        }
        return result;
    }
    return RSAKeyPair;
});
