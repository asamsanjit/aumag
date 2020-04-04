  function result()
        {
          var hour=new Date().getHour();
          var greeting;
          if (hour<18)
          {
            greeting="Good day";
          }
          else
          {
            greeting="Good evening";
          }
          document.getElementById("demo").innerHTML=greeting;
        }