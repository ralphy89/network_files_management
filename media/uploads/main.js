async function getTemperature(name) {
    const url = "https://jsonmock.hackerrank.com/api/weather?name="+name;
    console.log(url)
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const json = await response.json();
      temp = json['data'][0]['weather'].split(" ")[0];
      console.log(temp);
    } catch (error) {
      console.error(error.message);
    }
    
  }

  getTemperature("Dallas")