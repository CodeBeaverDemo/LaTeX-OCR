import importlib
import pathlib
import setuptools
import pytest

def dummy_setup(**kwargs):
    """A dummy setup function to capture setup attributes."""
    global setup_config
    setup_config = kwargs

@pytest.fixture(autouse=True)
def reset_setup_config():
    """Reset the global setup_config before each test."""
    global setup_config
    setup_config = {}

def test_setup_configuration(monkeypatch):
    """Test that setup configuration is correctly passed to setuptools.setup."""
    # Monkey patch setuptools.setup with dummy_setup and fake reading of README.md
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)

    # Check basic configuration
    assert setup_config.get('name') == 'pix2tex'
    assert setup_config.get('version') == '0.1.2'
    assert setup_config.get('author') == 'Lukas Blecher'
    assert setup_config.get('author_email') == 'luk.blecher@gmail.com'
    # Verify that the long description is taken from the patched read_text
    assert setup_config.get('long_description') == "Dummy long description"

def test_extras_require(monkeypatch):
    """Test that extras_require is correctly defined in setup configuration."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)

    extras = setup_config.get('extras_require')
    assert extras is not None, "extras_require should be defined"
    # Check that all expected keys are present
    for key in ['all', 'gui', 'api', 'train', 'highlight']:
        assert key in extras, f"extras_require missing key: {key}"
    # Check that the 'all' extras include items from 'gui'
    assert isinstance(extras['all'], list)
    assert len(extras['all']) >= len(extras['gui'])

def test_entry_points(monkeypatch):
    """Test that entry_points are correctly defined in setup configuration."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)

    entry_points = setup_config.get('entry_points')
    assert entry_points is not None, "entry_points should be defined"
    assert 'console_scripts' in entry_points, "entry_points should define console_scripts"
    scripts = entry_points['console_scripts']
    # Verify that all expected console script entries are present
    expected_scripts = [
        'pix2tex_gui = pix2tex.__main__:main',
        'pix2tex_cli = pix2tex.__main__:main',
        'latexocr = pix2tex.__main__:main',
        'pix2tex = pix2tex.__main__:main',
    ]
    for script in expected_scripts:
        assert script in scripts, f"Missing console script: {script}"

def test_package_data(monkeypatch):
    """Test that package_data is defined correctly in setup configuration."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)

    package_data = setup_config.get('package_data')
    assert package_data is not None, "package_data should be defined"
    # Verify that the package 'pix2tex' has the expected data file patterns
    assert 'pix2tex' in package_data, "package_data should contain the 'pix2tex' key"
    data_files = package_data['pix2tex']
    expected_patterns = ['resources/*', 'model/settings/*.yaml', 'model/dataset/*.json']
    for pattern in expected_patterns:
        assert pattern in data_files, f"Missing package data pattern: {pattern}"
def test_install_requires(monkeypatch):
    """Test that install_requires is correctly defined in setup configuration."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)

    install_requires = setup_config.get('install_requires')
    assert install_requires is not None, "install_requires should be defined"
    expected_deps = [
            'tqdm>=4.47.0',
            'munch>=2.5.0',
            'torch>=1.7.1',
            'opencv_python_headless>=4.1.1.26',
            'requests>=2.22.0',
            'einops>=0.3.0',
            'x_transformers==0.15.0',
            'transformers>=4.18.0',
            'tokenizers>=0.13.0',
            'numpy>=1.19.5',
            'Pillow>=9.1.0',
            'PyYAML>=5.4.1',
            'pandas>=1.0.0',
            'timm==0.5.4',
            'albumentations>=0.5.2',
            'pyreadline3>=3.4.1; platform_system=="Windows"',
    ]
    for dep in expected_deps:
            assert dep in install_requires, f"Missing dependency: {dep}"

def test_classifiers_and_keywords(monkeypatch):
    """Test that classifiers and keywords are correctly defined in setup configuration."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)

    classifiers = setup_config.get('classifiers')
    assert classifiers is not None, "classifiers should be defined"
    expected_classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
    for classifier in expected_classifiers:
        assert classifier in classifiers, f"Missing classifier: {classifier}"

    keywords = setup_config.get('keywords')
    assert keywords is not None, "keywords should be defined"
    expected_keywords = [
        'artificial intelligence',
        'deep learning',
        'image to text'
    ]
    for keyword in expected_keywords:
        assert keyword in keywords, f"Missing keyword: {keyword}"
def test_metadata(monkeypatch):
    """Test that metadata fields such as description, license, url, and long_description_content_type are correctly set."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)
    assert setup_config.get('description') == 'pix2tex: Using a ViT to convert images of equations into LaTeX code.'
    assert setup_config.get('license') == 'MIT'
    assert setup_config.get('url') == 'https://github.com/lukas-blecher/LaTeX-OCR/'
    assert setup_config.get('long_description_content_type') == 'text/markdown'

def test_find_packages(monkeypatch):
    """Test that packages are correctly set by monkey patching setuptools.find_packages."""
    # Monkey patch find_packages to return a known package list
    monkeypatch.setattr(setuptools, 'find_packages', lambda: ['pix2tex'])
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)
    assert setup_config.get('packages') == ['pix2tex']

def test_empty_long_description(monkeypatch):
    """Test that an empty README produces an empty long_description."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)
    assert setup_config.get('long_description') == ""
def test_extras_require_all_composition(monkeypatch):
    """Test that 'all' extras is exactly the concatenation of gui, api, train, and highlight extras."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)
    extras = setup_config.get('extras_require')
    expected_all = extras['gui'] + extras['api'] + extras['train'] + extras['highlight']
    assert extras['all'] == expected_all, "The 'all' extras must match the concatenated lists of gui, api, train, and highlight extras"

def test_setup_call_twice(monkeypatch):
    """Test that reloading the setup module twice produces the same configuration."""
    monkeypatch.setattr(setuptools, 'setup', dummy_setup)
    monkeypatch.setattr(pathlib.Path, 'read_text', lambda self, encoding: "Dummy long description")
    import pix2tex.setup as setup_module
    importlib.reload(setup_module)
    first_setup = setup_config.copy()
    importlib.reload(setup_module)
    second_setup = setup_config.copy()
    assert first_setup == second_setup, "Reloading the setup module should produce identical configuration"