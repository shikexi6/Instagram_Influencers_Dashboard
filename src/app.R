library(shiny)
library(plotly)
library(dplyr)
library(readr)

# Load dataset
data <- read_csv("../data/processed/influencers.csv")

# Convert necessary columns to numeric
data$posts <- as.numeric(gsub("[^0-9.]", "", data$posts))
data$followers <- as.numeric(gsub("[^0-9.]", "", data$followers))
data$influence_score <- as.numeric(gsub("[^0-9.]", "", data$influence_score))
data$eng_rate <- as.numeric(gsub("[^0-9.]", "", data$eng_rate)) / 100  # Convert percentage to decimal

# UI
ui <- fluidPage(
    # Custom CSS for styling
    tags$style(HTML("
        body { background-color: #f4f6f9; } /* Light grey background */
        .main-container { background: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px #ccc; }
        .sidebar { background: #34495e; color: white; padding: 15px; border-radius: 10px; }
        .sidebar .shiny-input-container { color: white; }
        .plot-container { background: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px #bbb; }
        h3 { color: #2c3e50; }
        .select-country { width: 100%; }
        .dashboard-text { font-size: 14px; color: #ecf0f1; margin-top: 10px; }
        .github-link a { color: #1abc9c; text-decoration: none; font-weight: bold; }
        .github-link a:hover { text-decoration: underline; }
    ")),
    
    titlePanel("📊 Interactive Influencer Data Dashboard"),
    
    sidebarLayout(
        sidebarPanel(
            class = "sidebar",
            h4("🌍 Select Country:"),
            selectInput("country", "", choices = c("", unique(data$country)), selected = "", width = "100%"),
            
            # Dashboard description
            div(class = "dashboard-text",
                h4("📢 About This Dashboard"),
                p("This interactive dashboard visualizes influencer data, including their engagement rates, 
                   number of posts, followers, and influence scores."),
                p("Use the country filter above to refine the data. 
                   The charts update automatically to show trends and key insights."),
                p("Trend lines help you identify patterns, and tooltips provide extra details when you hover over points.")
            ),
            
            # GitHub Link
            div(class = "github-link",
                h4("🔗 Github Repo:"),
                a("Instagram_Influencers_Dashboard", 
                  href = "https://github.com/shikexi6/Instagram_Influencers_Dashboard.git", 
                  target = "_blank")
            ),
            
            width = 2  # Narrower sidebar
        ),
        
        mainPanel(
            class = "main-container",
            width = 10,  # Make main panel take more space
            fluidRow(
                column(6, 
                       div(class = "plot-container",
                           h3("Influence Score vs. Posts"),
                           plotlyOutput("scatter_influence_posts", height = "450px")
                       )
                ),
                column(6, 
                       div(class = "plot-container",
                           h3("Engagement Rate vs. Posts"),
                           plotlyOutput("scatter_engagement_posts", height = "450px")
                       )
                )
            ),
            fluidRow(
                column(6, 
                       div(class = "plot-container",
                           h3("Influence Score vs. Followers"),
                           plotlyOutput("scatter_influence_followers", height = "450px")
                       )
                ),
                column(6, 
                       div(class = "plot-container",
                           h3("Top 5 Influencers by Followers"),
                           plotlyOutput("bar_influencer", height = "450px")
                       )
                )
            )
        )
    )
)


# Server
server <- function(input, output) {
    
    # Filtered dataset
    filtered_data <- reactive({
        if (input$country != "") {
            data %>% filter(country == input$country)
        } else {
            data
        }
    })
    
    # Scatter Plot: Influence Score vs. Posts (Interactive)
    output$scatter_influence_posts <- renderPlotly({
        plot_ly(filtered_data(), x = ~posts, y = ~influence_score, type = "scatter", mode = "markers",
                marker = list(size = 8, color = "blue"),
                hoverinfo = "text",
                text = ~paste("Country:", country, "<br>Posts:", posts, "<br>Influence Score:", influence_score)) %>%
            layout(xaxis = list(title = "Number of Posts"), yaxis = list(title = "Influence Score"))
    })
    
    # Scatter Plot: Engagement Rate vs. Posts (Interactive)
    output$scatter_engagement_posts <- renderPlotly({
        plot_ly(filtered_data(), x = ~posts, y = ~eng_rate, type = "scatter", mode = "markers",
                marker = list(size = 8, color = "green"),
                hoverinfo = "text",
                text = ~paste("Country:", country, "<br>Posts:", posts, "<br>Engagement Rate:", eng_rate)) %>%
            layout(xaxis = list(title = "Number of Posts"), yaxis = list(title = "Engagement Rate"))
    })
    
    # Scatter Plot: Influence Score vs. Followers (Interactive)
    output$scatter_influence_followers <- renderPlotly({
        plot_ly(filtered_data(), x = ~followers, y = ~influence_score, type = "scatter", mode = "markers",
                marker = list(size = 8, color = "purple"),
                hoverinfo = "text",
                text = ~paste("Country:", country, "<br>Followers:", followers, "<br>Influence Score:", influence_score)) %>%
            layout(xaxis = list(title = "Number of Followers"), yaxis = list(title = "Influence Score"))
    })
    
    # Bar Plot: Top 5 Influencers by Followers (Interactive)
    output$bar_influencer <- renderPlotly({
        top_5 <- filtered_data() %>% 
            arrange(desc(followers)) %>% 
            head(5)
        
        plot_ly(top_5, x = ~followers, y = ~reorder(channel_info, followers), type = "bar", orientation = "h",
                marker = list(color = "royalblue"),
                hoverinfo = "text",
                text = ~paste("Channel:", channel_info, "<br>Followers:", followers, "<br>Influence Score:", influence_score)) %>%
            layout(xaxis = list(title = "Followers"), yaxis = list(title = "Channel"))
    })
}

# Run App
shinyApp(ui = ui, server = server)

