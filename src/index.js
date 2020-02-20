import _ from 'lodash';
import './style.css';

function mainDiv() {
  const mainDiv = document.createElement('div');
  mainDiv.id = 'main_content';

  const titleDiv = document.createElement('div');
  titleDiv.classList.add('title');
  titleDiv.appendChild(document.createElement('span')).innerHTML = 'Json Explorer';
  titleDiv.appendChild(document.createElement('label'));
  mainDiv.appendChild(titleDiv);



  return mainDiv;
}

document.body.appendChild(mainDiv());
