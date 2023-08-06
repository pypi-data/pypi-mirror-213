from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fp:
    readme = fp.read()

setup(
    #開発者
    author="Nishi Kosei",
    #ライブラリの名前
    name="s2l2cardgames",
    #ライブラリのバージョン
    version="0.1.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    #パッケージの名前を自動で取得してくれる
    packages=[
    's2l2cardgames'
    ],
    # 依存関係がある場合ここにリストアップ
    install_requires=[
    ],
    #PyPIで検索時に利用されるライセンスやPythonバージョンのキーサード
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    #インストール時のPythonのバージョンの制約
    python_requires=">=3.6",
)