#!/usr/bin/env python
import sys
import re

class LuhnyBinParser:
    """
    Here are the variables sufficient to maintain state of computation
    - mBufferedString: Entire buffered sequence of characters so far. Can only contain digits, - or space
    - mLastSixteen: At most last sixteen characters. Can only contain digits
    - mFreshSum: Sum of every alternate digit AFTER current digit is processed
    - mStaleSum: Sum of every alternate digit BEFORE current digit is processed
    """
    

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Sets all state variables to default values
        """
        self.mBufferedString = ""
        self.mLastSixteen = ""
        self.mFreshDoubleSum = 0
        self.mStaleDoubleSum = 0
        self.mFreshSum = 0
        self.mStaleSum = 0

    def parseChar(self, c):
        """
        Main state machine. Parses every character.
        - If it's a non-digit-non-space, simply reset everything and return buffered string. It can not be Luhny sequence!
        - If it is - or space, simply buffer
        - Digits have special treatment in parseDigit
        """
        try:
            digit = int(c)
	    return self.parseDigit(digit)
        except:
            if c == "-" or c == " ":
                self.mBufferedString += c
                return ""
            else:
                retstr = self.mBufferedString + c
                self.reset()
                return retstr


    def swapStaleFresh(self):
        """
        Swapping stale and fresh after parsing every digit
        """
        temp = self.mFreshDoubleSum
        self.mFreshDoubleSum = self.mStaleDoubleSum
        self.mStaleDoubleSum = temp
        temp = self.mFreshSum
        self.mFreshSum = self.mStaleSum
        self.mStaleSum = temp


    def replaceX(self, oldstr):
        """
        Once successful Luhny sequence is found, replace all digits by X and keep spaces/- intact
        """
        return re.sub("[0-9]", "X", oldstr)

    
    def purgeBuffered(self, replaceX):
        """
        This method is called if you have come to a conclusion that the current buffer should be printed - either by replacing
        all digits by X or as it is. The boolean input replaceX tell you that
        """
        oldstr = self.mBufferedString
        self.mBufferedString = ""
        if replaceX:
            return self.replaceX(oldstr)
        else:
            return oldstr

    def parseDigit(self, digit):
        self.swapStaleFresh()
        double_digit = digit * 2
        self.mStaleDoubleSum += double_digit / 10 + double_digit % 10
        self.mFreshSum += digit
        self.mBufferedString += str(digit)
        self.mLastSixteen += str(digit)
        if len(self.mLastSixteen) < 14:
            return ""
        elif len(self.mLastSixteen) == 14:
            if (self.mFreshDoubleSum + self.mFreshSum) % 10 == 0:
                return self.purgeBuffered(True)
            else:
                return ""
        elif len(self.mLastSixteen) == 15:
            if (self.mFreshDoubleSum + self.mFreshSum) % 10 == 0:
                return self.purgeBuffered(True)
            else:
                first_digit = int(self.mLastSixteen[0])
                double_digit = first_digit * 2
                temp = self.mFreshDoubleSum - (double_digit / 10 + double_digit % 10)
                if temp % 10 == 0:
                    retStr = self.mBufferedString[0:1] + self.replaceX(self.mBufferedString[1:])
                    self.mBufferedString = ""
                    return retStr
                else:
                    return ""
        elif len(self.mLastSixteen) == 16:
            if self.mFreshDoubleSum % 10 == 0:
                return self.purgeBuffered(True)
            else:
                second_digit = int(self.mLastSixteen[1])
                double_digit = second_digit * 2
                temp = self.mFreshDoubleSum - (double_digit / 10 + double_digit % 10)
                if temp % 10 == 0:
                    retStr = self.mBufferedString[0:2] + self.replaceX(self.mBufferedString[2:])
                    self.mBufferedString = ""
                    return retStr
                else:
                    return self.purgeBuffered(False)
        else:
            stale_num = int(self.mLastSixteen[0])
            self.mLastSixteen = self.mLastSixteen[1:]
            double_digit = stale_num * 2
            self.mStaleDoubleSum -= (double_digit / 10 + double_digit % 10)
            return ""


if __name__ == "__main__":
    l = LuhnyBinParser()
    for c in raw_input():
        sys.stdout.write(l.parseChar(c))
    sys.stdout.write(l.mBufferedString + "\n")
