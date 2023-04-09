from fouine.core._helper import Target as Target


class DEFAULT_CONFIG:
    """Default configuration. It extracts RegistryHives System and User (including SYSTEM and SECURiTY logs), Browsers Data, and MFT.
    Based on https:/github.com/Velocidex/velociraptor/blob/master/artifacts/definitions/Windows/KapeFiles/Targets.yaml .

    It includes the following rules:

       219-257 Chrome/n
       258-259 ChromeExtensions/n
       260     ChromeFileSystem/n
       261     Edge/n
       262-283 EdgeChromium/n
       284-318 Firefox/n
       319-331 InternetExplorer/n
       484-485 MFT/n
       613-653 RegistryHivesSystem/n
       654-662 RegistryHivesUser/n

    Attributes:
       output(str): Local dir where data extracted from targets will be saved. Corresponds to --output.
       Targets(list): List of targets for the default configurations. Hardcoded.
    """

    def __init__(self, output: str):
        self.output = output
        self.Targets = [
            [
                ##### MFT ##### Rules 484-485
                # rule 484
                Target(
                    name="$MFT",
                    category="MFT",
                    path="",
                    file_mask="$MFT",
                    recursive=False,
                    export_path=self.output,
                ),
                # rule 485
                Target(
                    name="$MFTMirr",
                    category="MFT",
                    path="",
                    file_mask="$MFTMirr",
                    recursive=False,
                    export_path=self.output,
                ),
                ##### REGISTRIES #####
                ### RegistryHiveSystem: Rules 613-653
                # 613
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SAM.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 614
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SAM.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 615 ### LOGS
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SECURITY.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 616 ### LOGS
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SECURITY.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 617
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SOFTWARE.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 618
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SOFTWARE.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 619 ### LOGS
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SYSTEM.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 620 ### LOGS
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SYSTEM.LOG*",
                    recursive=False,
                    export_path=self.output,
                ),
                # 621
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SAM",
                    recursive=False,
                    export_path=self.output,
                ),
                # 622
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SAM",
                    recursive=False,
                    export_path=self.output,
                ),
                # 623
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SECURITY",
                    recursive=False,
                    export_path=self.output,
                ),
                # 624
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SECURITY",
                    recursive=False,
                    export_path=self.output,
                ),
                # 625
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SOFTWARE",
                    recursive=False,
                    export_path=self.output,
                ),
                # 626
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SOFTWARE",
                    recursive=False,
                    export_path=self.output,
                ),
                # 627
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="SYSTEM",
                    recursive=False,
                    export_path=self.output,
                ),
                # 628
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="SYSTEM",
                    recursive=False,
                    export_path=self.output,
                ),
                # 629
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/RegBack/",
                    file_mask="*.LOG",
                    recursive=False,
                    export_path=self.output,
                ),
                # 630
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/RegBack/",
                    file_mask="*.LOG",
                    recursive=False,
                    export_path=self.output,
                ),
                # 631
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/RegBack/",
                    file_mask="SAM",
                    recursive=True,
                    export_path=self.output,
                ),
                # 632
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/RegBack/",
                    file_mask="SAM",
                    recursive=True,
                    export_path=self.output,
                ),
                # 633
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/RegBack/",
                    file_mask="SECURITY",
                    recursive=True,
                    export_path=self.output,
                ),
                # 634
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/RegBack/",
                    file_mask="SECURITY",
                    recursive=True,
                    export_path=self.output,
                ),
                # 635
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/RegBack/",
                    file_mask="SOFTWARE",
                    recursive=True,
                    export_path=self.output,
                ),
                # 636
                Target(
                    name="",
                    category="",
                    path="/Registry,Windows.old/Windows/System32/config/RegBack/",
                    file_mask="SOFTWARE",
                    recursive=True,
                    export_path=self.output,
                ),
                # 637
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/RegBack/",
                    file_mask="SYSTEM",
                    recursive=True,
                    export_path=self.output,
                ),
                # 638
                Target(
                    name="",
                    category="",
                    path="/,Windows.old/Windows/System32/config/RegBack/",
                    file_mask="SYSTEM",
                    recursive=True,
                    export_path=self.output,
                ),
                # 639
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/RegBack/",
                    file_mask="SYSTEM1",
                    recursive=True,
                    export_path=self.output,
                ),
                # 640
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/RegBack/",
                    file_mask="SYSTEM1",
                    recursive=True,
                    export_path=self.output,
                ),
                # 641
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/systemprofile/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 642
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/systemprofile/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 643
                Target(
                    name="",
                    category="",
                    path="/Registry,Windows/System32/config/systemprofile/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 644
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/systemprofile/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 645
                Target(
                    name="",
                    category="",
                    path="/Windows/ServiceProfiles/LocalService/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 646
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/ServiceProfiles/LocalService/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 647
                Target(
                    name="",
                    category="",
                    path="/Windows/ServiceProfiles/LocalService/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 648
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/ServiceProfiles/LocalService/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 649
                Target(
                    name="",
                    category="",
                    path="/Windows/ServiceProfiles/NetworkService/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 650
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/ServiceProfiles/NetworkService/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 651
                Target(
                    name="",
                    category="",
                    path="/Windows/ServiceProfiles/NetworkService/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 652
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/ServiceProfiles/NetworkService/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 653
                Target(
                    name="",
                    category="",
                    path="/System Volume Information/_restore*/RP*/snapshot/",
                    file_mask="_REGISTRY_*",
                    recursive=True,
                    export_path=self.output,
                ),
                ### RegistryHiveUser: Rules 654 - 662
                # 654
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 655
                Target(
                    name="",
                    category="",
                    path="/Users/*/",
                    file_mask="NTUSER.DAT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 656
                Target(
                    name="",
                    category="",
                    path="/Users/*/",
                    file_mask="NTUSER.DAT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 657
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="DEFAULT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 658
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="DEFAULT",
                    recursive=True,
                    export_path=self.output,
                ),
                # 659
                Target(
                    name="",
                    category="",
                    path="/Windows/System32/config/",
                    file_mask="/DEFAULT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 660
                Target(
                    name="",
                    category="",
                    path="/Windows.old/Windows/System32/config/",
                    file_mask="DEFAULT.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 661
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Microsoft/Windows/",
                    file_mask="UsrClass.dat",
                    recursive=True,
                    export_path=self.output,
                ),
                # 662
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Microsoft/Windows/",
                    file_mask="UsrClass.dat.LOG*",
                    recursive=True,
                    export_path=self.output,
                ),
                ### BROWSERS DATA
                ## CHROME
                # Browser: Rules  219-257
                # 219
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Bookmarks*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 220
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Cookies*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 221
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Current Session",
                    recursive=True,
                    export_path=self.output,
                ),
                # 222
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Current Tabs",
                    recursive=True,
                    export_path=self.output,
                ),
                # 223
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Favicons*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 224
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="History*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 225
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Last Session",
                    recursive=True,
                    export_path=self.output,
                ),
                # 226
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Last Tabs",
                    recursive=True,
                    export_path=self.output,
                ),
                # 227
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Login Data",
                    recursive=True,
                    export_path=self.output,
                ),
                # 228
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Preferences",
                    recursive=True,
                    export_path=self.output,
                ),
                # 229
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Shortcuts*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 230
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Top Sites*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 231
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Visited Links",
                    recursive=True,
                    export_path=self.output,
                ),
                # 232
                Target(
                    name="",
                    category="",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/",
                    file_mask="Web Data*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 233
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*",
                    file_mask="Bookmarks*",
                    recursive=True,
                    export_path=self.output,
                ),
                # 234
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/**10/Cookies*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 235
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Current Session",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 236
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Current Tabs",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 237
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/DownloadMetadata",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 238
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Extension Cookies",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 239
                Target(
                    name="",
                    category="",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Favicons*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 240
                Target(
                    name="Chrome History",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/History*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 241
                Target(
                    name="Chrome Last Session",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Last Session",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 242
                Target(
                    name="Chrome Last Tabs",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Last Tabs",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 243
                Target(
                    name="Chrome Sessions Folder",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Sessions/*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 244
                Target(
                    name="Chrome Login Data",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Login Data",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 245
                Target(
                    name="Chrome Media History",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Media History*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 246
                Target(
                    name="Chrome Network Action Predictor",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Network Action Predictor",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 247
                Target(
                    name="Chrome Network Persistent State",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Network Persistent State",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 248
                Target(
                    name="Chrome Preferences",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Preferences",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 249
                Target(
                    name="Chrome Quota Manager",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/QuotaManager",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 250
                Target(
                    name="Chrome Reporting and NEL",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Reporting and NEL",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 251
                Target(
                    name="Chrome Shortcuts",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Shortcuts*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 252
                Target(
                    name="Chrome Top Sites",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Top Sites*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 253
                Target(
                    name="Chrome Trust Tokens",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Trust Tokens*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 254
                Target(
                    name="Chrome SyncData Database",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Sync Data/SyncData.sqlite3",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 255
                Target(
                    name="Chrome Visited Links",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Visited Links",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 256
                Target(
                    name="Chrome Web Data",
                    category="Communications",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Web Data*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 257
                Target(
                    name="Windows Protect Folder",
                    category="FileSystem",
                    path="/Users/*/AppData/Roaming/Microsoft/Protect/*/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # Extensions: Rules 258-259
                # 258
                Target(
                    name="Chrome Extension Files",
                    category="Communication",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/Extensions/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 259
                Target(
                    name="Chrome Extension Files XP",
                    category="Communications",
                    path="/Documents and Settings/*/Local Settings/Application Data/Google/Chrome/User Data/*/Extensions/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # FileSystem: Rule 260
                # 260
                Target(
                    name="Chrome HTML5 File System Folder",
                    category="Communication",
                    path="/Users/*/AppData/Local/Google/Chrome/User Data/*/File System/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                ## EDGE
                # Edge: Rule 261
                # 261
                Target(
                    name="Edge folder",
                    category="Communications",
                    path="/Users/*/AppData/Local/Packages/Microsoft.MicrosoftEdge_8wekyb3d8bbwe/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # Edge Chromium: Rules 262-283
                # 262
                Target(
                    name="Edge bookmarks",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Bookmarks*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 263
                Target(
                    name="Edge Collections",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Collections/collectionsSQLite",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 264
                Target(
                    name="Edge Cookies",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Cookies*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 265
                Target(
                    name="Edge Current Session",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Current Session",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 266
                Target(
                    name="Edge Current Tabs",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Current Tabs",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 267
                Target(
                    name="Edge Favicons",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Favicons*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 268
                Target(
                    name="Edge History",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/History*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 269
                Target(
                    name="Edge Last Session",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Last Session",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 270
                Target(
                    name="Edge Last Tabs",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Last Tabs",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 271
                Target(
                    name="Edge Sessions Folder",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Sessions/*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 272
                Target(
                    name="Edge Login Data",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Login Data",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 273
                Target(
                    name="Edge Media History",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Media History*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 274
                Target(
                    name="Edge Network Action Predictor",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Network Action Predictor",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 275
                Target(
                    name="Edge Preferences",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Preferences",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 276
                Target(
                    name="Edge Shortcuts",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Shortcuts*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 277
                Target(
                    name="Edge Top Sites",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Top Sites*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 278
                Target(
                    name="Edge SyncData Database",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Sync Data/SyncData.sqlite3",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 279
                Target(
                    name="Edge Bookmarks",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Bookmarks*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 280
                Target(
                    name="Edge Visited Links",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Visited Links",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 281
                Target(
                    name="Edge Web Data",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/*/Web Data*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 282
                Target(
                    name="Windows Protect Folder",
                    category="FileSystem",
                    path="/Users/*/AppData/Roaming/Microsoft/Protect/*/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 283
                Target(
                    name="Edge Snapshots Folder",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Edge/User Data/Snapshots/*/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                ## FIREFOX: Rules 284-318
                # 284
                Target(
                    name="Addons",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/addons.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 285
                Target(
                    name="Bookmarks",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/weave/bookmarks.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 286
                Target(
                    name="Bookmarks",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/bookmarkbackups/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 287
                Target(
                    name="Cookies",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 288
                Target(
                    name="Cookies",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/firefox_cookies.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 289
                Target(
                    name="Downloads",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/downloads.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 290
                Target(
                    name="Extensions",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/extensions.json",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 291
                Target(
                    name="Favicons",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/favicons.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 292
                Target(
                    name="Form history",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/formhistory.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 293
                Target(
                    name="Permissions",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/permissions.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 294
                Target(
                    name="Places",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/places.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 295
                Target(
                    name="Protections",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/protections.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 296
                Target(
                    name="Search",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/search.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 297
                Target(
                    name="Signons",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/signons.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 298
                Target(
                    name="Storage Sync",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/storage-sync.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 299
                Target(
                    name="Webappstore",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/webappstore.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 300
                Target(
                    name="Password",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/key*.db",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 301
                Target(
                    name="Password",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/signon*.*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 302
                Target(
                    name="Password",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/logins.json",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 303
                Target(
                    name="Preferences",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/prefs.js",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 304
                Target(
                    name="Sessionstore",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/sessionstore*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 305
                Target(
                    name="Sessionstore Folder",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Mozilla/Firefox/Profiles/*/sessionstore-backups/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 306
                Target(
                    name="Places XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/places.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 307
                Target(
                    name="Downloads XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/downloads.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 308
                Target(
                    name="Form history XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/formhistory.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 309
                Target(
                    name="Cookies XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/cookies.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 310
                Target(
                    name="Signons XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/signons.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 311
                Target(
                    name="Webappstore XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/webappstore.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 312
                Target(
                    name="Favicons XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/favicons.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 313
                Target(
                    name="Addons XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/addons.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 314
                Target(
                    name="Search XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/search.sqlite*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 315
                Target(
                    name="Password XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/key*.db",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 316
                Target(
                    name="Password XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/signon*.*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 317
                Target(
                    name="Password XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/logins.json",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 318
                Target(
                    name="Sessionstore XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Mozilla/Firefox/Profiles/*/sessionstore*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # EXPLORER: Rules 319-331
                # 319
                Target(
                    name="Index.dat History",
                    category="Communications",
                    path="/Documents and Settings/*/Local Settings/History/History.IE5/index.dat",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 320
                Target(
                    name="Index.dat History subdirectory",
                    category="Communications",
                    path="/Documents and Settings/*/Local Settings/History/History.IE5/*/index.dat",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 321
                Target(
                    name="Index.dat cookies",
                    category="Communications",
                    path="/Documents and Settings/*/Cookies/index.dat",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 322
                Target(
                    name="Index.dat UserData",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Microsoft/Internet Explorer/UserData/index.dat",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 323
                Target(
                    name="Index.dat Office XP",
                    category="Communications",
                    path="/Documents and Settings/*/Application Data/Microsoft/Office/Recent/index.dat",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 324
                Target(
                    name="Index.dat Office",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Microsoft/Office/Recent/index.dat",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 325
                Target(
                    name="Local Internet Explorer folder",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Internet Explorer/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 326
                Target(
                    name="Roaming Internet Explorer folder",
                    category="Communications",
                    path="/Users/*/AppData/Roaming/Microsoft/Internet Explorer/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 327
                Target(
                    name="IE 9/10 History",
                    category="Communications",
                    path="",
                    file_mask="Users/*/AppData/Local/Microsoft/Windows/History/**10",
                    recursive=True,
                    export_path=self.output,
                ),
                # 328
                Target(
                    name="IE 9/10 Cookies",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Windows/Cookies/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 329
                Target(
                    name="IE 9/10 Download History",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Windows/IEDownloadHistory/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 330
                Target(
                    name="IE 11 Metadata",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Windows/WebCache/*",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
                # 331
                Target(
                    name="IE 11 Cookies",
                    category="Communications",
                    path="/Users/*/AppData/Local/Microsoft/Windows/INetCookies/**10",
                    file_mask="",
                    recursive=True,
                    export_path=self.output,
                ),
            ],
        ]
