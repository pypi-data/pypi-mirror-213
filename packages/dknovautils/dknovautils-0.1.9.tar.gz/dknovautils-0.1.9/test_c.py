import dknovautils as dku

from dknovautils.dkat import AT
from dknovautils.myadd import m_add
print(AT.VERSION)

assert m_add(1, 2) == 3
