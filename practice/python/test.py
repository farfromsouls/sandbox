class Solution:
    def isPalindrome(self, s):
        s = ''.join([l.lower() for l in s if l.isalpha()])
        for i in range(0, (len(s) // 2) + 1):
            l1 = s[i]
            l2 = s[len(s)-1-i]
            
            if i < len(s)-1-i:
                if l1 != l2:
                    return False
            else:
                if l1 == l2:
                    return True
        
x = Solution()
print(x.isPalindrome("0P"))