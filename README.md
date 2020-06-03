# doc-builder

Used by Drone to build documentation website.

# Usage

The `entrypoint.sh` program is in charge of cloning the right repository and  run a script name `build.sh` that is in charge of building the documentation, and publish it.

Program to build and publish the documentation for a repo can be added in a folder named `/build/<REPO_NAME>` of this project.

Once cloned, all files found in the `/build/<REPO_NAME>` folder are copied to the `/<REPO_NAME>/` folder, and the `build.sh` file is run.

# Trigger 

`drone.yml` file: 

```yaml

kind: pipeline
name: default

steps:
  - name: Build Cortex-Neurons documentation
    image: thehiveproject/doc-builder
  when:
    branch:
    - event: [tag]
```


# Websites 

## Cortex-Analyzers

Programs are set in `/build/Cortex-Analyzers` folder.

`build.sh` call a second program called `generate.py` that:
 
    - generates all .md files, one for each neuron in the `Cortex-Analyzers/docs` folder
    - copies some existing .md files in the `docs/` folder
    - generates a `mkdocs.yml`

Then, run `mkdocs gh-deploy`. 

The documentation can be seen at [](https://thehive-project.github.io/Cortex-Analyzers/).

