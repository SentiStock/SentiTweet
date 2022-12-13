const csrf_token = $('input[name="csrfmiddlewaretoken"]').attr('value')

async function toggle_favorite(obejct_type, object_id) {
  const url = "/api/favorite/"
  const options = {
    method: 'POST',
    body: JSON.stringify({
      object_type: obejct_type,
      object_id: object_id,
    }),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token,
    }
  }
  data = await fetch(url, options)
    .then(function (response) {
      if (response.ok) {
        return response.json();
      }
      return Promise.reject(response);
    }).then(function (data) {
      return data
    }).catch(function (error) {
      console.warn('Something went wrong.', error);
    });
  if (data.success == 'favorited') {
    $("#favoriteButton > i:nth-child(1)").attr('class', 'feather icon-star-on')
  } else if (data.success == 'unfavorited') {
    $("#favoriteButton > i:nth-child(1)").attr('class', 'feather icon-star')
  }
}

// $("#searchTable").on("keyup", function() {
//   var value = $(this).val().toLowerCase();
//   $("#listAllTable tr").filter(function() {
//       $(this).toggle($(this).text()
//       .toLowerCase().indexOf(value) > -1)
//   });
// });


$("#searchAllInput").on("keyup", function () {
  var value = $(this).val().toLowerCase();
  search_all(value)
});

$("#searchTableCompanies").on("keyup", function () {
  var value = $(this).val().toLowerCase();
  search_companies(value)
});

$("#searchTableHashtags").on("keyup", function () {
  var value = $(this).val().toLowerCase();
  search_hashtags(value)
});

$("#searchTableTwitterUsers").on("keyup", function () {
  var value = $(this).val().toLowerCase();
  search_twitterusers(value)
});


async function fetch_objects(query, objects) {
  var url = "/api/search/?query=" + query + "&objects=" + objects
  return await fetch(url)
    .then(function (response) {
      if (response.ok) {
        return response.json();
      }
      return Promise.reject(response);
    }).then(function (data) {
      console.log(data)
      return data.data
    }).catch(function (error) {
      console.warn('Something went wrong.', error);
    });
}

async function search_all(query) {
  data = await fetch_objects(query = query, objects = 'company,hashtag,set,twitteruser')
  companies = data.companies
  hashtags = data.hashtags
  sets = data.sets
  twitterusers = data.twitterusers

  $("#searchAllDropdown li").remove()
  companies.slice(0, 10).forEach((company) => {
    li = '<li><a class="dropdown-item" href="/companies/' + company.symbol + '/">'
    li += '<span class="pcoded-micon"><i class="feather icon-bar-chart-2"></i></span><span'
    li += 'class="pcoded-mtext">' + company.name + '</span>'
    li += '</a></li>'
    $("#searchAllDropdown").append(li)
  })
  hashtags.slice(0, 10).forEach((hashtag) => {
    li = '<li><a class="dropdown-item" href="/hashtags/' + hashtag.clean_value + '/">'
    li += '<span class="pcoded-micon"><i class="feather icon-hash"></i></span><span'
    li += 'class="pcoded-mtext">' + hashtag.clean_value + '</span>'
    li += '</a></li>'
    $("#searchAllDropdown").append(li)
  })
  sets.slice(0, 10).forEach((set) => {
    li = '<li><a class="dropdown-item" href="/sets/' + set.id + '/">'
    li += '<span class="pcoded-micon"><i class="feather icon-slack"></i></span><span'
    li += 'class="pcoded-mtext">' + set.name + '</span>'
    li += '</a></li>'
    $("#searchAllDropdown").append(li)
  })
  twitterusers.slice(0, 10).forEach((twitteruser) => {
    li = '<li><a class="dropdown-item" href="/twitterusers/' + twitteruser.id + '/">'
    li += '<span class="pcoded-micon"><i class="feather icon-user"></i></span><span'
    li += 'class="pcoded-mtext">' + twitteruser.username + '</span>'
    li += '</a></li>'
    $("#searchAllDropdown").append(li)
  })
}

async function search_companies(query) {
  data = await fetch_objects(query = query, objects = 'company')
  companies = data.companies

  $('#listAllTableCompanies tr').remove()

  th = '<tr>'
  th += '<th ></th>'
  th += '<th >Company name and symbol</th>'
  th += '<th>Total Tweets</th>'
  th += '<th>Unique Hashtags</th>'
  th += '<th>Last updated</th>'
  th += '<th>Total Followers</th>'
  th += '</tr>'

  $("#listAllTableCompanies").append(th)

  companies.slice(0, 50).forEach((company) => {
    tr = '<tr class="unread">'
    tr += '<td>'
    tr += '<a href="' + company.symbol + '/">'
    tr += '<i class="far fa-building text-c-blue f-28"></i>'
    tr += '</a>'
    tr += '</td>'
    tr += '<td>'
    tr += '<a href="' + company.symbol + '/">'
    tr += '<h6 class="mb-1">' + company.name + '</h6>'
    tr += '<p class="m-0">' + company.symbol + '</p>'
    tr += '</a>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + company.tweet_count + ' Tweets</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + company.hashtag_count + ' Hashtags</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="text-muted">'
    if (company.is_up_to_date) tr += '<i class="fas fa-circle text-c-green f-10 m-r-15">'
    else tr += '<i class= "fas fa-circle text-c-red f-10 m-r-15">'
    tr += '</i>'
    tr += company.newest_tweet.post_date
    tr += '</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + company.favorite_count + ' Followers</h6>'
    tr += '</td>'
    tr += '</tr>'
    $("#listAllTableCompanies").append(tr)
  })
}

async function search_twitterusers(query) {
  data = await fetch_objects(query = query, objects = 'twitteruser')
  twitterusers = data.twitterusers

  $('#listAllTableTwitterUsers tr').remove()

  th = '<tr>'
  th += '<th ></th>'
  th += '<th >Username</th>'
  th += '<th>Total Tweets</th>'
  th += '<th>Created sets</th>'
  th += '<th>Last updated</th>'
  th += '<th>Total Followers</th>'
  th += '</tr>'

  $("#listAllTableTwitterUsers").append(th)

  twitterusers.slice(0, 9000).forEach((twitteruser) => {
    tr = '<tr class="unread">'
    tr += '<td>'
    tr += '<a href="' + twitteruser.id + '/">'
    tr += ' <i class="feather icon-user text-c-green f-30 m-r-10"></i>'
    tr += '</a>'
    tr += '</td>'
    tr += '<td>'
    tr += '<a href="' + twitteruser.id + '/">'
    tr += '<h6 class="mb-1">' + twitteruser.username + '</h6>'
    tr += '</a>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + twitteruser.tweet_count + ' Tweets</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + twitteruser.verified + ' isVerified</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="text-muted">'
    if (twitteruser.is_up_to_date) tr += '<i class="fas fa-circle text-c-green f-10 m-r-15">'
    else tr += '<i class= "fas fa-circle text-c-red f-10 m-r-15">'
    tr += '</i>'
    tr += twitteruser.newest_tweet.post_date
    tr += '</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + twitteruser.favorite_count + ' Followers</h6>'
    tr += '</td>'
    tr += '</tr>'
    $("#listAllTableTwitterUsers").append(tr)
  })
}

async function search_hashtags(query) {
  data = await fetch_objects(query = query, objects = 'hashtag')
  hashtags = data.hashtags

  $('#listAllTableHashtags tr').remove()

  th = '<tr>'
  th += '<th ></th>'
  th += '<th >Hashtag</th>'
  th += '<th>Total Tweets</th>'
  th += '<th>Contained in sets</th>'
  th += '<th>Last updated</th>'
  th += '<th>Total Followers</th>'
  th += '</tr>'

  $("#listAllTableHashtags").append(th)

  hashtags.slice(0, 100).forEach((hashtag) => {
    tr = '<tr class="unread">'
    tr += '<td>'
    tr += '<a href="' + hashtag.clean_value + '/">'
    tr += '<i class="feather icon-hash text-c-red f-30 m-r-10"></i>'
    tr += '</a>'
    tr += '</td>'
    tr += '<td>'
    tr += '<a href="' + hashtag.clean_value + '/">'
    tr += '<h6 class="mb-1">' + hashtag.value + '</h6>'
    tr += '</a>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + hashtag.tweet_count + ' Tweets</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + hashtag.set_count + ' Sets</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="text-muted">'
    if (hashtag.is_up_to_date) tr += '<i class="fas fa-circle text-c-green f-10 m-r-15">'
    else tr += '<i class= "fas fa-circle text-c-red f-10 m-r-15">'
    tr += '</i>'
    tr += hashtag.newest_tweet.post_date
    tr += '</h6>'
    tr += '</td>'
    tr += '<td>'
    tr += '<h6 class="mb-1">' + hashtag.favorite_count + ' Followers</h6>'
    tr += '</td>'
    tr += '</tr>'
    $("#listAllTableHashtags").append(tr)
  })
}