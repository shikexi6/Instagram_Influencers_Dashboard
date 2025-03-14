# Instagram Influencer Dashboard

## DSCI-532-2025-21

### Author: Kexin Shi (Coco)

## Motivation

**Target Audience: Social media analysts, marketers, and influencers**

Instagram plays a pivotal role in shaping public opinion and influencing user behavior. Understanding how content spreads, which topics gain traction, and the impact of different engagement strategies is crucial for marketers, content creators, and analysts. This dashboard enables users to explore Instagram network trends, identify key influencers, and analyze engagement patterns. By visualizing how content is shared, liked, and commented on, users can gain insights into audience behavior and optimize their strategies for better reach and impact.

## Usage

### Video Walkthrough
Take a look at the video instruction:

![](img/demo.mp4)

### Dashboard
Try the live demo::

https://019591e1-cb2f-508b-568c-753d8f287dce.share.connect.posit.cloud/

### Developer Guide

1. Clone the git repository from GitHub

In your terminal, please run the following command:

```bash
git clone https://github.com/shikexi6/Instagram_Influencers_Dashboard.git
```

2.  Conda environment setup

To set up the necessary packages for running the code, you need to create a virtual environment by using conda with the environment file under the root directory:

```bash
conda env create --file environment.yaml
```

3.  Running the dash app locally

You can run the dash app by typing 
``` bash
Rscript -e "shiny::runApp('src/app.R')"
```

You can view the dash app by navigating to the address ``http://127.0.0.1:6897` in your browser.


## License

- The project code is licensed under the [MIT License](https://opensource.org/license/MIT). See the [LICENSE](https://github.com/shikexi6/Instagram_Influencers_Dashboard/blob/main/LICENSE) file for details.

- The project report is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license](https://creativecommons.org/licenses/by-nc-nd/4.0/).

If re-using or re-mixing this project, please ensure proper attribution and adherence to the terms of the respective licenses.

## Contributing

Please see the [Contributing Guidelines](CONTRIBUTING.md) for proper procedures to contribute to our project.

If you encounter issues or have suggestions, feel free to open an issue in the repo.