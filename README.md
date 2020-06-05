# doc-builder

Used by Drone to build documentation website.

# Usage

The `entrypoint.sh` runs script named `build.sh` with the `PLUGIN_TYPE` variable. This programs is in charge of building specific documentation from some repositories like [Cortex-Neurons](https://github.com/TheHive-Project/Cortex-Analyzers/).

Program to build and publish a specific documentation for a repo should be added in a folder named `/build/<type>` of this project. The `type` value is set in Drone and read as `PLUGIN_TYPE`. 

The program can also be run as a command line:

```bash
./build/<type>/build.sh <TYPE>
```

## Trigger 

`drone.yml` file: 

```yaml

kind: pipeline
name: default

steps:
  - name: Prepare documentation files
    image: thehiveproject/doc-builder
    settings:
      - type: <type>
    when:
      branch:
      - event: [tag]
```

## Existing types

- `Cortex-Neurons` for [Cortex-Neurons](https://github.com/TheHive-Project/Cortex-Analyzers/) repository.
