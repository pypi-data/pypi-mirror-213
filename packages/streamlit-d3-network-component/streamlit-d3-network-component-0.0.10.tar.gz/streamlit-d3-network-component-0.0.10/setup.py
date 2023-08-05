import setuptools

setuptools.setup(
    name="streamlit-d3-network-component",
    version="0.0.10",
    author="Andras Gyacsok",
    author_email="andras.gyacsok@boehringer-ingelheim.com",
    description="This package is a Streamlit custom component to represent network diagram using D3.js",
    long_description="This package is the custom Streamlit component to visualise network graphs using D3.js",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)