const graphe = document.querySelector('#graphs');
let graphval = "pie";
    
const monthid1 = document.querySelector("#monthss");
let monthval1 = 6;   
const renderchart= (data,labels,typ) => {
    const ctx = document.getElementById('myChart').getContext('2d');

    const myChart = new Chart(ctx, {
        type: typ,
        data: {
            labels:labels,
            datasets: [{
                label:`display Income`,
                data: data,
                backgroundColor: [ 
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(128,0,128,0.2)',
                  'rgba(0,128,128,0.2)',
                  'rgba(0,255, 0 ,0.2)',
  
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }], 
        },
        options: {
            title: {
              display: true,
              text: "Income Distribution ",
              fontSize: 25,fontColor: "#fff",
            },
            legend: {
              display: true,
              position: "right",
              labels: {
                fontColor: "#fff",
              },
            },
          },
     
    });
    // myChart.destroy();
    if(myChart == undefined)
  myChart.destroy();
    }


monthid1.addEventListener("change",(e)=>{
  monthval1=e.target.value;
  console.log(monthval1)

    const getCharData=()=>{
        console.log("fetching  ");
        fetch("/income/income_source_summary",{
          body: JSON.stringify({ month : monthval1 }),
          method: "POST",
        })
        .then(res => res.json())
        .then(results =>{
          console.log("results: ",results);
          const source_data = results.income_source_data;
          const [labels,data]=[Object.keys(source_data),Object.values(source_data)]
          renderchart(data,labels,graphval);
         
        })
    }
  
    document.onload = getCharData();
  });

  graphe.addEventListener("change",(e)=>{
    graphval=e.target.value;
    const getCharData=()=>{
      console.log("fetching ");
      fetch("/income/income_source_summary",{
        body: JSON.stringify({ month : monthval1 }),
        method: "POST",
      })
      .then(res => res.json())
      .then(results =>{
        console.log("results: ",results);
        const category_data = results.income_source_data;
        const [labels,data]=[Object.keys(category_data),Object.values(category_data)]
        renderchart(data,labels,graphval);
      })
    }
    console.log(monthval1);
    document.onload = getCharData();
})
const source = document.querySelector('#source');

source.addEventListener("change",(e)=>{
 let sourceval=e.target.value;
  console.log(sourceval);

  const getCharData=()=>{
    console.log("fetching ");
    fetch("/income/income_one_source_summary",{
      body: JSON.stringify({nsource : sourceval , month : monthval1}),
      method: "POST",
    })
    .then(res => res.json())
    .then(results =>{
      graphval = "line";
      console.log("results: ",results);
      const category_data = results.income_source_data;
      const [labels,data]=[Object.keys(category_data),Object.values(category_data)]
      renderchart(data,labels,graphval);
    })
  }
  document.onload = getCharData();
})


  const getCharData=()=>{
    console.log("fetching  ");
    fetch("/income/income_source_summary")
    .then(res => res.json())
    .then(results =>{
      console.log("results: ",results);
      const source_data = results.income_source_data;
      const [labels,data]=[Object.keys(source_data),Object.values(source_data)]
      renderchart(data,labels,graphval);
     
    })
}

document.onload = getCharData();