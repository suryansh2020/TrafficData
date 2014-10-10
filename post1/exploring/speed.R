# set working drive
setwd("/home/tbonza/projects/TrafficData/MassDOThack/Road_RTTM_Volume")
pair_definitions <- read.csv("pair_definitions.csv") #get data

## Refresher on slicing arrays
pair_definitions[1:6,6]

# data from pair_routes.xml
pairId <- c('5490','5491','5493','5494','5495','5496','5497','5498',
            '5499','5500')

time <- c(695.96389591268,578.44739225705, 634.9935992859,
          236.9999753125, 478.7864422849,561.60000943866,
          567.95611862845,344.99989732146,136.00001042146,
          255.00014756953)

speed <- c(78.1,77.2,74.8,72.9,75.9,76.3,71.0,73.0,76.8,50.8)

# data from pair_definitions.csv
distance <- c(15.1,12.4,13.2,4.8,10.1,11.9,11.2,7,2.9,3.6)


# speed
mph <- function(time, distance){return(((time/60)/distance)*100)}

# test output +- buffer in mph
test <- function(mph,speed, buffer){
  if(speed - buffer < mph && speed + buffer > mph){return(TRUE)}
  else {return(FALSE)}}

mphDist <- function(mph,speed){
  return(abs(speed - mph))
}



# not quite sure how to do this in R
testRun <- function(time,distance,speed,buffer){
  count <- 1
  while (count < length(time)){
    test(mph(time[count],distance[count]),
         speed[count],buffer)
    count = count + 1
  }
}

buffer <- 5
#answer <- testRun(time,distance,speed, buffer)

count <- 5 # 3,4 is false
test(mph(time[count],distance[count]),
         speed[count],buffer)

hmm <- function(){
  count <- 1
  ans <- c()
  while(count < 5){
    ans <- c(ans,count)
    count = count + 1
  }
  return(ans)
}

## test function to see how well it does
testMphDist <- function(time,distance, speed){
  count <- 1
  ans <- c()
  while(count <= length(speed)){
    ans <- c(ans,
             mphDist(mph(time[count],
                         distance[count]),
                     speed[count]))
    
    
    count = count + 1
  }
  return(ans)
}

# run the test, looks good; let's use it.
summary(testMphDist(time,distance,speed))


# output histogram to pdf
#pdf("testRun.pdf")
#hist(testMphDist(time,distance,speed))
#dev.off()
