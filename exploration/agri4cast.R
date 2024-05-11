agri4cast <- read.csv("data/source/df_ch.csv", sep = ";")

summary(agri4cast)
dim(agri4cast)

ggplot(data = agri4cast) +
  geom_line(mapping = aes(DAY, DAY)) +
  labs(title = "Linearität Tagesfolge")

library(dplyr)

agri4cast %>%
  group_by(DAY, GRID_NO) %>%
  count() %>%
  ggplot(aes(DAY, n)) +
  geom_line() +
  labs(title = "Anzahl messwerte pro Tag, pro Grid")

agri4cast %>%
  group_by(DAY, GRID_NO) %>%
  mutate(PRECIPITATIONSUM = sum(PRECIPITATION),
         DATE = as.Date(sprintf("%s", DAY), format = "%Y%m%d")) %>%
  select(PRECIPITATIONSUM, DATE, GRID_NO) %>%
  ggplot(aes(x = DATE, y = PRECIPITATIONSUM, color = factor(GRID_NO))) +
  geom_histogram(stat = "identity", binwidth = 10) +
  labs("Histogramm Summe Regenfall pro grid number, über Zeit (Tage)")

agri4cast %>%
  group_by(DAY, GRID_NO) %>%
  mutate(PRECIPITATIONSUM = sum(PRECIPITATION),
         MONTH = format(as.Date(sprintf("%s", DAY), format = "%Y%m%d"), "%Y%m")) %>%
  select(PRECIPITATIONSUM, MONTH, GRID_NO) %>%
  group_by(MONTH) %>%
  ggplot(aes(x = MONTH, y = PRECIPITATIONSUM, color = factor(GRID_NO))) +
  geom_histogram(stat = "identity", binwidth = 10) +
  labs("Histogramm Summe Regenfall pro grid number, über Zeit (Monate)")


agri4cast %>%
  group_by(GRID_NO) %>%
  mutate(
    MONTH = format(as.Date(sprintf("%s", DAY), format = "%Y%m%d"), "%Y%m")) %>%
  group_by(MONTH) %>%
  mutate(PRECIPITATIONSUM = sum(PRECIPITATION)) %>%
  select(PRECIPITATIONSUM, MONTH) %>%
  distinct(PRECIPITATIONSUM, MONTH) %>%
  print(n=10) %>%
  ggplot(aes(x=MONTH, y=PRECIPITATIONSUM)) +
  geom_col() +
  labs(title = "Summed precipation per month")

agri4cast %>%
  group_by(GRID_NO) %>%
  mutate(PRECIPITATIONSUM = sum(PRECIPITATION)) %>%
  print(n=100) %>%
  ggplot(aes(x=GRID_NO,y=PRECIPITATIONSUM)) +
  geom_histogram(stat = "identity", binwidth = 10)

unique(agri4cast$GRID_NO)
class(agri4cast$GRID_NO)