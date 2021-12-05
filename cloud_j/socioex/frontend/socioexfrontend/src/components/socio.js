import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import axiosInstance from "../axios";
import Button from "@mui/material/Button";
import Customtable from "./table";
import Chart from "react-google-charts";
import { radioClasses } from "@mui/material";

export default function MultilineTextFields() {
  const [value, setValue] = React.useState("");
  const [tweets, updatedTweets] = React.useState([]);
  const [emotions, updatedEmotions] = React.useState([]);
  const [imageLabels, updatedImageLables] = React.useState([
    [
      "Entity",
      "Percentage",
      { role: "style" },
      {
        sourceColumn: 0,
        role: "annotation",
        type: "string",
        calc: "stringify",
      },
    ],
  ]);

  const [gotimage, updatedgotimage] = React.useState(false);

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const params = new URLSearchParams({
      user: value,
    }).toString();

    axiosInstance
      .get(`get-user-tweets/?` + params)
      .then((res) => {
        console.log(res);
        updatedTweets([res.data]);
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
      .get(`get-user-tone/?` + params)
      .then((res) => {
        console.log(res);
        // for(var i=0; i<res.data.length; i++){
        //   var tone = res.data[i]["tweet_tone"]["tone"]
        //   var per = res.data[i]["tweet_tone"]["percent"]
        //   var x = emotions[tone] + per
        //   updatedEmotions({ ...emotions, emotions["tone"]: x })
        // }
        updatedEmotions(res.data["arr"]);
      })
      .catch((err) => {
        console.log(err);
      });

    axiosInstance.get(`get-user-images/?` + params).then((res) => {
      updatedImageLables([...imageLabels, ...res.data["array"]]);
      updatedgotimage(true);
    });
  };

  React.useEffect(() => {
    console.log(imageLabels);
  }, [imageLabels]);

  return (
    <>
      <Box
        component="form"
        sx={{
          "& .MuiTextField-root": { m: 1, width: "25ch" },
          display: "flex",
          justifyContent: "center",
        }}
        noValidate
        autoComplete="off"
      >
        <div
          style={{
            marginTop: "20px",
            display: "flex",
            flexDirection: "column",
            alignItem: "center",
            justifyContent: "center",
          }}
        >
          <TextField
            id="outlined-multiline-flexible"
            label="Username"
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
            style={{ width: "90%", marginLeft: "10px", marginTop: "5%" }}
          >
            Submit
          </Button>
        </div>
      </Box>

      <br></br>

      {tweets.length > 0 && (
        <>
          <Customtable tablerows={tweets[0]} />

          <Button
            type="text"
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleAnalyze}
            style={{ marginTop: "30px", width: "200px", marginBottom: "30px" }}
          >
            Analyze
          </Button>
        </>
      )}

      {/* <Customtable tablerows={tweets[0]} />

                <Button
                    type="text"
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleAnalyze}
                >
                    Analyze
                </Button> */}

      <div style={{ display: "flex", justifyContent: "center" }}>
        {emotions.length > 0 && (
          <Chart
            width={"800px"}
            height={"600px"}
            chartType="PieChart"
            loader={<div>Loading Chart</div>}
            data={emotions}
            options={{
              title: "Emotion chart",
              // Just add this option
              is3D: true,
            }}
            rootProps={{ "data-testid": "2" }}
          />
        )}

        {gotimage && (
          <Chart
            width={"800px"}
            height={"600px"}
            chartType="BarChart"
            loader={<div>Loading Chart</div>}
            data={imageLabels}
            options={{
              title: "Image labels",
              width: 800,
              height: 600,
              bar: { groupWidth: "95%" },
              legend: { position: "none" },
            }}
            // For tests
            rootProps={{ "data-testid": "6" }}
          />
        )}
      </div>
    </>
  );
}
