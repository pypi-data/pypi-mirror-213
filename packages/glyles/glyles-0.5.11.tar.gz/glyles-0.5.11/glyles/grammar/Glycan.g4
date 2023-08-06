grammar Glycan;

start:
    '{' branch glycan ' ' TYPE '}'
    | '{' branch glycan '}'
    | '{' glycan ' ' TYPE '}'
    | '{' glycan '}';
branch:
    glycan CON
    | glycan CON branch
    | '[' branch ']'
    | glycan CON '[' branch ']' branch
    | glycan CON '[' branch ']' '[' branch ']' branch
    | glycan CON '[' branch ']' '[' branch ']' '[' branch ']' branch;
glycan:
    deriv RING TYPE | deriv TYPE | deriv RING | deriv;
deriv:
    SAC+ RING TYPE MOD* | SAC+ TYPE MOD* | SAC+ RING MOD* | SAC+ MOD*
    | MOD+ SAC+ RING TYPE MOD* | MOD+ SAC+ TYPE MOD* | MOD+ SAC+ RING MOD* | MOD+ SAC+ MOD*;

SAC:
    COUNT | 'Glc' | 'Man' | 'Gal' | 'Gul' | 'Alt' | 'All' | 'Tal' | 'Ido' | 'Qui' | 'Rha' | 'Fuc' | 'Oli' | 'Tyv'
    | 'Abe' | 'Par' | 'Dig' | 'Col' | 'Ara' | 'Lyx' | 'Xyl' | 'Rib' | 'Kdn' | 'Neu' | 'Sia' | 'Pse' | 'Leg' | 'Aci'
    | 'Bac' | 'Kdo' | 'Dha' | 'Mur' | 'Api' | 'Fru' | 'Tag' | 'Sor' | 'Psi' | 'Ery' | 'Thre' | 'Rul' | 'Xul' | 'Unk'
    | 'Ace' | 'Aco' | 'Asc' | 'Fus' | 'Ins' | 'Ko' | 'Pau' | 'Per'| 'Sed' | 'Sug' | 'Vio' | 'Xlu' | 'Yer' | 'Erwiniose';
MOD:
    NUM ',' NUM '-Anhydro-' | NUM '-Anhydro-'
    | NUM '-' BRIDGE '-' FG '-'
    | NUM CARB
    | NUM BRIDGE* FG
    | (NUM | BRIDGE* | '-') FG
    | NUM ('d' | 'e') | NUM ',' NUM 'd'
    | '-ulosaric' | '-ulosonic' | '-uronic' | '-onic' | '-aric' | '-ol'
    | '0d' | 'D-' | 'L-';
FG:
    COUNT | 'Ceroplastic' | 'Lacceroic' | '3oxoMyr' | 'Psyllic' | 'Geddic' | 'Allyl' | 'Phthi'
    | 'aLnn' | 'gLnn' | 'eSte' | 'Coum' | 'HSer' | 'Prop'
    | 'Ach' | 'Aep' | 'Ala' | 'Ang' | 'Asp' | 'Beh' | 'But' | 'Cct' | 'Cer' | 'Cet' | 'Cho' | 'Cin' | 'Crt' | 'Cys'
    | 'Dce' | 'Dco' | 'Dec' | 'Dhp' | 'Dod' | 'Etg' | 'EtN' | 'Etn' | 'Fer' | 'Gro' | 'Glu' | 'Gly' | 'Hpo' | 'Hse'
    | 'Hxo' | 'Lac' | 'Lau' | 'Leu' | 'Lin' | 'Lys' | 'Mal' | 'Mar' | 'Mel' | 'Mon' | 'Myr' | 'Ner' | 'Nno' | 'Non'
    | 'Oco' | 'Ole' | 'Orn' | 'Pam' | 'Pro' | 'Pyr' | 'Ser' | 'Sin' | 'Ste' | 'tBu' | 'Thr' | 'Tig' | 'Und' | 'Vac'
    | 'Udo' | 'Ulo' | 'ulo'
    | 'Ac' | 'Am' | 'Bn' | 'Br' | 'Bu' | 'Bz' | 'Cl' | 'Cm' | 'DD' | 'DL' | 'DL-' | 'Et' | 'Fo' | 'Gc' | 'Hp' | 'Hx'
    | 'LD' | 'LL' | 'Me' | 'Nn' | 'Oc' | 'Pe' | 'Ph' | 'Pr' | 'Pp' | 'Tf' | 'Tr' | 'Ts' | 'Vl' | 'en'
    | 'A' | 'N' | 'F' | 'I' | 'S' | 'P';
BRIDGE:
    'C' | 'N' | 'O' | 'P';
CARB:
    ('ai' | 'a' | 'i')? 'C' NUM ADD*;
ADD:
    '=' '{' CT? NUM (',' CT? NUM)* '}' | 'c' '{' NUM (',' NUM)* '}';
COUNT:
    'Hep' | 'Hex' | 'Oct' | 'Pen' | 'Suc';
CON:
    '(' TYPE NUM '-' NUM ')'
    | '(' NUM '-' NUM ')'
    | TYPE NUM '-' NUM
    | TYPE NUM;
TYPE:
    'a' | 'b';
CT:
    'c' | 't';
RING:
    'p' | 'f';
NUM:
    ('1'..'9') DIGIT*;
DIGIT:
    ('0'..'9');

// antlr -Dlanguage=Python3 Glycan.g4
