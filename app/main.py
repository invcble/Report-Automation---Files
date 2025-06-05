import dataclean
import dataprocess



SELF_DAT_PATH = "2025\\SelfDat.csv"
PEER_DAT_PATH = "2025\\PeerDat.csv"
LOGO_PATH      = "app\\Merck_Logo.png"
TEMPLATE_PATH  = "app\\Merk_Talent_Incubator.pdf"

# This path is constant
combined_csv_path = "CombinedDataNational_py.csv"

dataclean.clean(self_path=SELF_DAT_PATH, peer_path=PEER_DAT_PATH)
dataprocess.process(combined_path=combined_csv_path, feedback_path=PEER_DAT_PATH, logo_path=LOGO_PATH, template_path=TEMPLATE_PATH)
