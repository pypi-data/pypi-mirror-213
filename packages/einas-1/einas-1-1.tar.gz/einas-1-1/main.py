from setuptools import setup

base_package_name = "einas"
num_packages = 2
common_summary = "This is a sample package generated with a common summary."

# Iterate over the range of package numbers
for package_number in range(1, num_packages + 1):
    # Generate the package name
    package_name = f"{base_package_name}-{package_number}"

    # Define the package details
    package_info = dict(
        name=package_name,
        version=package_number,
        description=common_summary,
    )

    # Create the package distribution
    setup(**package_info)
