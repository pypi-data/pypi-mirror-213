import setuptools

setuptools.setup(
    name="st_pop_up_component",
    version="0.0.3",
    author="Siva S",
    author_email="",
    description="Using this component",
    long_description='''import streamlit as st
                    import st_pop_up_component as sp
                    output =sp.st_custom_pop_up("Do you want to cancel?",key="first-key")
                    st.write(output)''',
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
