import lrparsing
from lrparsing import Keyword, List, Prio, Ref, THIS, Token, Tokens


class CardSearchParser(lrparsing.Grammar):
    #
    # Put Tokens we don't want to re-type in a TokenRegistry.
    #
    class T(lrparsing.TokenRegistry):
        ident = Token(re="[A-Za-z_][A-Za-z_0-9]*:")
        field_val = Token(re=r'[^:()|&~]+|"[^"]+"')

    #
    # Grammar rules.
    #
    expr = Ref("expr")
    atom = T.ident + T.field_val | Token('(') + expr + ')'
    expr = Prio(
        atom,
        Tokens("~") >> THIS,
        THIS << Tokens("& |") << THIS,
    )
    START = expr


"""
Example expression:
z:legendary&s:rat|r:"+1/+1 counter"
"""
