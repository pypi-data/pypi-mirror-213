from setuptools import setup, Extension

# Define the extension module
extension_module = Extension(
    'gpu_control',
    sources=['gpu_control/gpu_control_wrapper.cpp', 'gpu_control/gpu_control.cpp'],
    include_dirs=['gpu_control'],
    libraries=['nvml'],
    library_dirs=['gpu_control'],
)

# Setup
setup(
    name='gpu_control',
    version='1.0.0',
    description='NVIDIA GPU temp and fan control',
    author='Hans',
    author_email='no.mail@example.com',
    url='https://github.com/d0nk3yhm/gpu_controller',
    ext_modules=[extension_module],
    packages=['gpu_control'],
    install_requires=['numpy'],
)
