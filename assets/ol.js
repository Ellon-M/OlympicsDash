summerBtn = document.getElementById('summer-btn');
winterBtn = document.getElementById('winter-btn');

summerBtn.addEventListener('click', () => {
    document.getElementById('left-col').style.backgroundColor('#fcf8e6');

    const repsStat = document.getElementById('rep-stats-card-sec');
    repsStat.style.backgroundColor('#ffc496');
    repsStat.setProperty('filter', 'drop-shadow(8px 8px 4px #ffb47a) contrast(120%)');
    
    const decStat = document.getElementById('dec-stats-card')
    decStat.style.backgroundColor('#c7b98d');
    decStat.setProperty('filter', 'drop-shadow(8px 8px 4px #c4a643) contrast(120%)')

    const partStat = document.getElementById('ev-part-stats-card-sec')
    partStat.style.backgroundColor('#c9784d');
    partStat.setProperty('filter', 'drop-shadow(8px 8px 4px #bf5e2a) contrast(120%)')

    const wonStat = document.getElementById('ev-won-stats-card-sec')
    wonStat.style.backgroundColor('#f2f2b6');
    wonStat.setProperty('filter', 'drop-shadow(8px 8px 4px #e8e872) contrast(120%)')


