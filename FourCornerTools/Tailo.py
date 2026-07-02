# --------------------------------------#------------------------------------- #
# Provides class FcMakerTailo
# - a special FcMaker
# --------------------------------------#------------------------------------- #
import json
from .shared import FcMaker
from .configs import PATHS

# --------------------------------------#------------------------------------- #
class FcMakerTailo(FcMaker): 
    # ----------------------------------#------------------------------------- #
    def __init__(self):                 # initializer
        super().__init__('Tailo')
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def _sandhi(self, regs):            # modify sandhi
        if regs: 
            regs[-1].sandhi = '[last]'
        return regs
    # ----------------------------------#------------------------------------- #
    # ----------------------------------#------------------------------------- #
    def syllable_lister(self):          # list all syllables for .tex
        res = []
        
        with open(
            PATHS['ref'] / self.system_name / 'phonology.json',
            'r', encoding='utf-8'
        ) as fp:
            # tone definitions
            n_tones = ['1', '2', '3', '5', '6', '7']
            e_tones = ['4', '8']
            
            # load json
            phon = json.load(fp)
            
            # loop
            for onset in phon['ONSETS']: 
                for rime, rime_parts in phon['RIMES'].items():
                    tex_glide = rime_parts['glide']
                    tex_nucleus = rime_parts['nucleus']
                    tex_coda = rime_parts['coda']
                    
                    # consider palatalization for onset
                    tex_onset = f'{onset}i' if onset in {'tsh','ts','s','j'} and rime.startswith('i') else onset
                    
                    # coda-tone
                    tones = e_tones if rime[-1] in {'p','t','k','h'} else n_tones
                    for tone in tones: 
                        macro_name = f'{onset}{rime}{tone}'
                        
                        res.append(
                            f'\\expandafter\\newcommand\\csname Syllable{self.system_name}@{macro_name}\\endcsname[1]{{\\fc{self.system_name} {{#1}}{{{tex_onset}}}{{{tex_glide}}}{{{tex_nucleus}}}{{{tex_coda}{tone}}} }}'
                        )
        return res
    # ----------------------------------#------------------------------------- #
# --------------------------------------#------------------------------------- #