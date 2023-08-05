# Amazon ECS task definition rendering CLI <!-- omit in toc -->

A package for ECS task definition rendering.
From the idea of [GitHub action](https://github.com/aws-actions/amazon-ecs-render-task-definition), I've started to work on this little tool that is usable locally or from your runners with AWS role attached.
With this tool is possible to chose a profile to use, define the task definition family name and all the image uri to update in a single command.

**Table of Content**
<!-- toc -->
- [Installation](#installation)
- [Usage](#usage)
- [License Summary](#license-summary)
<!-- tocstop -->

## Installation
____
You can install the package using `pip install aws-ecs-task-render`.

## Usage
Once installed, it's possible to use the CLI simply running the command:
```
aws-ecs-task-render -p your_profile -f task_family_name -if image_name=new_image_uri
```
It's possible to update more than one image at time adding other key=value to the `-if` command like that:
```
aws-ecs-task-render -p your_profile -f task_family_name -if image_name_1=new_image_uri_1 image_name_2=new_image_uri_2
```
This tool can be used only to update an already existing container definition, it cannot add a new one.
It doesn't generate a new task definition, it only render it returning a cleaned json output usable for a new task definition creation.

## License Summary
This code is made available under the GPLv3 license.
