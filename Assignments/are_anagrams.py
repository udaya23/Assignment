# Returns True if two words are anagrams of each other; False otherwise.


class AreAnagrams:
    
    @staticmethod
    def are_anagrams(a, b):
       for i in range(0,len(a),1):
            if i in range(0,len(b),1):
                return True

print(AreAnagrams.are_anagrams('neural', 'unreal'))


