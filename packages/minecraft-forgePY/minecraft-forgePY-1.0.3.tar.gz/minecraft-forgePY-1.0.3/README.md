# 📦 minecraft-forgepy
A simple Python package to fetch latest and recommended download URLs of [Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/) website. 

## 💾 Installation 
```
pip install minecraft-forgepy 
```

## 🔍 How to use
```
import forgepy

latest = forgepy.GetLatestURL("1.19.4")
recommended = forgepy.GetRecommendedURL("1.19.4")
```

## ❗Disclaimer
- This package only supports Minecraft versions **1.5.2 and above**.
- original name for this package was supposed to be forgePY, but due to PyPi not letting me upload it, PyPi name is minecraft-forgepy. **But name forgepy is still and will be used in code!**

## 🤖 Source Code
- This project is licensed under GNU General Public License v3.0
- [GitHub repository](https://github.com/matejmajny/forge.py)