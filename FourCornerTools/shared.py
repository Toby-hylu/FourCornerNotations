# --------------------------------------#------------------------------------- #
# Provides class FcMaker
# - lister: generate .sty file from symbol.json and phonology.json
# - marker: generate .tex file from .txt file with chars marked
# What to modify: 
# - sandhi pattern: in function FcMaker.sandhi(regs)
# - syllable: in function FcMaker.syllable_lister()
#   - as the pattern of phonology.json 
# --------------------------------------#------------------------------------- #
import json
import re
from dataclasses import dataclass
from .configs import PATHS, PROJ_ROOT

# --------------------------------------#------------------------------------- #
def is_CJK(txt:str):
    pattern = re.compile(r'^[\u4e00-\u9fff]+$')
    return bool(pattern.match(txt))

def is_PUNCT(txt:str): 
    pattern = re.compile(r'^[\uff00-\uffef\u3000-\u303f]+$')
    return bool(pattern.match(txt))
# --------------------------------------#------------------------------------- #
# --------------------------------------#------------------------------------- #
@dataclass
class CharReg:
    char   : str
    ro     : str
    sandhi : str
    comment: str
    def to_tex(self, system_name) -> str:
        return f'\\Mark{{{self.char}}}{{\\Syllable{system_name}{self.sandhi}{{{self.ro}}}}}% {self.comment}\n'
# --------------------------------------#------------------------------------- #
# --------------------------------------#------------------------------------- #
class FcMaker: 
    # ----------------------------------#------------------------------------- #
    def __init__(                       # initializer
        self                           ,# Args: 
        name: str                      ,# - name of mapping system in ../json/
    )                                  :# Returns: None
        self.system_name = name
        self.source_path = PATHS['ref'] / self.system_name
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def lister(                         # generate list of symbols in .sty
        self                           ,# Args: 
        target=PROJ_ROOT               ,# - target path
    )                                  :# Returns: None
        with open(PROJ_ROOT / f'fc{self.system_name}.sty', 'w', encoding='utf-8') as fout:
            # step-0: write predefs
            fout.write(
f"""% Provides fc{self.system_name} package
% It maps {self.system_name} roman literation to four corner notations
%
\\ProvidesPackage{{fc{self.system_name}}}
\\RequirePackage{{fcframe}}
%
% frame macro
\\NewDocumentCommand{{\\Symbol{self.system_name}}}{{m}}{{\\csname Symbol{self.system_name}@#1\\endcsname}}
\\NewDocumentCommand{{\\Syllable{self.system_name}}}{{O{{}} m}}{{\\csname Syllable{self.system_name}@#2\\endcsname{{#1}}}}
\\NewDocumentCommand{{\\from{self.system_name}}}{{O{{}} m}}{{\\raisebox{{-.5em}}[0pt][0pt]{{\\Syllable{self.system_name}[#1]{{#2}}}}}}
%
\\makeatletter
% begin symbol list
%
"""
            )
            
            # step-1: list symbols
            fout.write('\n'.join(self.symbol_lister()))
            
            
            # step-2: special four corner display macros
            fout.write(
f"""
% end of symbol list
%
% four corner macros
%
\\NewDocumentCommand{{\\fc{self.system_name}}}{{m m m m m}}{{%
  \\FourCornerFrame{{#1}}%
    {{\\csname Symbol{self.system_name}@#2\\endcsname}}%
    {{\\csname Symbol{self.system_name}@#3\\endcsname}}%
    {{\\csname Symbol{self.system_name}@#4\\endcsname}}%
    {{\\csname Symbol{self.system_name}@#5\\endcsname}}%
}}%
%
% begin syllable list
%
\\newcommand{{\\Syllable{self.system_name}@}}{{}}
\\newcommand{{\\Syllable{self.system_name}@unknown}}{{?}}
%
"""
            )
            
            # step-3: list syllables
            fout.write('%\n'.join(self.syllable_lister()))
            
            # step-3: end input
            fout.write(f'%\n% end syllable list\n%\n\\makeatother\n\\endinput')
            
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def symbol_lister(                  # list all symbols for .tex
        self                           ,# Args: None
    )                                  :# Returns: List[str]
        # format string 'u3099u310B+u30FD' means:
        # \ooalign{\hss\char"3099\char"310B\cr\hss\char"30FD\cr}
        
        # format string 'u3099u310B' means: 
        # \char"3099\char"310B
        
        res = []
        
        with open(
            PATHS['ref'] / self.system_name / 'symbol.json', 
            'r', encoding='utf-8'
        ) as fs:
            symbols = json.load(fs)
            
            for k, v in symbols.items(): 
                macro_name = f'\\csname Symbol{self.system_name}@{k}\\endcsname'
                contents = []
                comments = []
                
                v_parts = v.split('+')  # see if there is ooalign
                
                for v_part in v_parts:  # deal with each aligned part
                    
                    comments.append(''.join([chr(int(code,16)) for code in v_part.split('u') if code]))
                    contents.append(v_part.replace('u','\\char\"'))
                
                comment = ' + '.join(comments)
                content = f'\\ooalign{{\\hss{'\\cr\\hss'.join(contents)}\\cr}}' if len(contents) > 1 else contents[0]
                res.append(f'\\expandafter\\newcommand{macro_name}{{{content}}}% {comment}')
        
        return res
            
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def syllable_lister(                # list all syllables for .tex
        self                           ,# Args: None
    )                                  :# Returns: List[str]
        raise NotImplementedError
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def marker(                         # mark .tex files from raw .txt files
        self                           ,# Args: 
        folder_name: str               ,# - Paths['raw'] / folder_name / *.txt
        dict_source: str               ,# - name of dictionary
        max_detect_length: int=4       ,# - longest word in dictionary
    )                                  :# Returns: None
        with open(
            PATHS['ref'] / self.system_name / f'{dict_source}.json', 
            'r', encoding='utf-8'
        ) as rin:
            # create target folder from source folder
            txt_source_folder = PATHS['raw'] / folder_name
            tex_target_folder = PATHS['out'] / folder_name
            tex_target_folder.mkdir(parents=True, exist_ok=True)
            print('... folder created ...')
            
            # load dictionary as json
            ref = json.load(rin)
            print('... dictionary loaded ...')
            
            # read .txt files and generate .tex files
            for txtfile in txt_source_folder.rglob('*.txt'): 
                # get name of the file, with '.txt' removed
                txtname = txtfile.name.split('.')[0]
                print(f'... found file {txtname}.txt ...')
                
                # open file_in and file_out
                with open(txtfile, 'r', encoding='utf-8') as fin,\
                     open(tex_target_folder/f'{txtname}.tex', 'w', encoding='utf-8') as fout: 
                    self._singlefilemarker(
                        fin, 
                        fout, 
                        ref,
                        max_detect_length=max_detect_length
                    )
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def _sandhi(                        # how to deal with sandhi 
        self                           ,# Args: 
        regs: list                     ,# - list of CharReg object
    )                                  :# Returns: list
        return regs                     # default: no sandhi
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def _singlefilemarker(              # logic of mark one single file
        self                           ,# Args:
        fin                            ,# - file in
        fout                           ,# - file out
        ref                            ,# - mark reference
        max_detect_length: int         ,# - longest word in dictionary
    )                                  :# Returns: None
        print('... starts writing single file ...')
        # parameters
        max_char_per_line = 26
        max_line_per_page = 8
        
        # counters and flags
        is_first_line = True
        char_count = 0
        
        # processing starts
        for line in fin: 
            # paragraph enter
            if is_first_line:
                is_first_line = False
            else: 
                fout.write('\\Large\\\\\\\\% paragraph enter\n')
            
            # for a new line, char_count is 0
            char_count = 0
            
            # greed match
            # use halfwidth space as tokenization mark
            remains = f'{line.strip()} '
            
            # record word until it encounters a space / punct
            regs = []
            
            while remains: 
                if is_CJK(remains[:1]): # requires mark
                    matched_chars = None
                    matched_ros   = None
                    matched_len   = 0
                    
                    # try matching
                    for l in range(max_detect_length, 0, -1): 
                        candidate = remains[:l]
                        if candidate in ref: 
                            matched_chars = candidate
                            matched_ros   = ref[candidate].split()
                            matched_len   = l
                            break
                    
                    if matched_chars is not None:
                        if len(matched_chars) != len(matched_ros): 
                            raise ValueError(f'dict error: {matched_words}: {matched_ros}')
                            
                        # append CharReg objects into regs
                        for char, ro in zip(matched_chars, matched_ros): 
                            regs.append(
                                CharReg(
                                    char, 
                                    ro, 
                                    '',
                                    'single!' if matched_len == 1 else ''
                                )
                            )
                        remains = remains[matched_len:]
                    else:               # not recorded, obviously it is single char
                        regs.append(
                            CharReg(
                                remains[0],
                                'unknown',
                                '',
                                'need update!'
                            )
                        )
                        remains = remains[1:]
                else:                   # space or punctuation
                    # check sandhi
                    # - modify self.sandhi(regs) if there is any
                    regs = self._sandhi(regs)
                    
                    # punctuations should also be printed
                    if is_PUNCT(remains[:1]): 
                        regs.append(
                            CharReg(
                                remains[0],
                                '',
                                '',
                                'punctuation'
                            )
                        )
                        
                    # write file
                    for reg in regs: 
                        fout.write(reg.to_tex(self.system_name))
                        char_count += 1
                        
                        # check enter
                        if char_count == max_char_per_line: 
                            fout.write(f'\\Large\\\\\\\\% line enter\n')
                            char_count = 0
                    
                    # clear after write
                    regs = []
                    
                    # remove the space or punctuation
                    remains = remains[1:]
        print('... ends writing ...')
    # ----------------------------------#------------------------------------- #
# --------------------------------------#------------------------------------- #