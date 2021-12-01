import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import axiosInstance from '../axios';
import Button from '@mui/material/Button';
import Customtable from './table';

export default function MultilineTextFields() {
    const [value, setValue] = React.useState('');
    const [tweets, updatedTweets] = React.useState([]);

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

    React.useEffect(() => {
      console.log(tweets);
    })

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
      </>
    );
}
