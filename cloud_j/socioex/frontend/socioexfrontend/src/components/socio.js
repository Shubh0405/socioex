import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import axiosInstance from '../axios';
import Button from '@mui/material/Button';
import Customtable from './table';
import Chart from "react-google-charts";

export default function MultilineTextFields() {
    const [value, setValue] = React.useState('');
    const [tweets, updatedTweets] = React.useState([]);
    const [emotions, updatedEmotions] = React.useState([]);

    const handleChange = (event) => {
        setValue(event.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const params = new URLSearchParams({
          user: value, 
        }).toString();

        axiosInstance
            .get(`get-user-tweets/?`+params)
            .then((res) => {
                console.log(res);
                updatedTweets([res.data])
            })
            .catch((err) => {
              console.log(err);
            });
    };

    const handleAnalyze = (e) => {
      e.preventDefault();

      const params = new URLSearchParams({
        user: value, 
      }).toString();

      axiosInstance
          .get(`get-user-tone/?`+params)
          .then((res) => {
              console.log(res);
              // for(var i=0; i<res.data.length; i++){
              //   var tone = res.data[i]["tweet_tone"]["tone"]
              //   var per = res.data[i]["tweet_tone"]["percent"]
              //   var x = emotions[tone] + per
              //   updatedEmotions({ ...emotions, emotions["tone"]: x })
              // }
              updatedEmotions(res.data["arr"])
          })
          .catch((err) => {
            console.log(err);
          });
  };

    React.useEffect(() => {
      console.log(emotions);
    },[emotions])

    return (
      <>
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '25ch' },
            }}
            noValidate
            autoComplete="off"
        >
            <div>
                <TextField
                    id="outlined-multiline-flexible"
                    label="Multiline"
                    multiline
                    maxRows={4}
                    value={value}
                    onChange={handleChange}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                >
                    Submit
                </Button>
            </div>
        </Box>

        <br></br>

        <Customtable tablerows={tweets[0]} />

        {/* {
          (() => {
              console.log("before")
            if(tweets[0]){
                console.log("after")
              return(
                <Customtable tablerows={tweets[0]} />
              )
            }
          })
        } */}

                <Button
                    type="text"
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleAnalyze}
                >
                    Analyze
                </Button>

      {
        emotions.length > 0 && 
        <Chart
        width={'500px'}
        height={'300px'}
        chartType="PieChart"
        loader={<div>Loading Chart</div>}
        data={emotions}
        options={{
          title: 'Emotion chart',
          // Just add this option
          is3D: true,
        }}
        rootProps={{ 'data-testid': '2' }}
      />
      }


{/* <Chart
  width={'500px'}
  height={'300px'}
  chartType="BarChart"
  loader={<div>Loading Chart</div>}
  data={[
    [
      'Entity',
      'Percentage',
      { role: 'style' },
      {
        sourceColumn: 0,
        role: 'annotation',
        type: 'string',
        calc: 'stringify',
      },
    ],
    ['Copper', 8.94, '#b87333', null],
    ['Silver', 10.49, 'silver', null],
    ['Gold', 19.3, 'gold', null],
    ['Platinum', 21.45, 'color: #e5e4e2', null],
  ]}
  options={{
    title: 'Image labels',
    width: 600,
    height: 400,
    bar: { groupWidth: '95%' },
    legend: { position: 'none' },
  }}
  // For tests
  rootProps={{ 'data-testid': '6' }}
/> */}

      </>
    );
}
