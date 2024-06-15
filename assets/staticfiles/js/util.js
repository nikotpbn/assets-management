const toastLiveExample = document.getElementById("liveToast");
const toastLiveBody = document.querySelector(".toast-body");

export const displayToastCustomMessage = (message, status) => {
  if (status === 200) {
    toastLiveExample.classList.remove("text-bg-danger");
    toastLiveExample.classList.add("text-bg-success");
  } else {
    toastLiveExample.classList.remove("text-bg-success");
    toastLiveExample.classList.add("text-bg-danger");
  }
  toastLiveBody.innerHTML = message;
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
  toastBootstrap.show();
};

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const sendRequest = async (url, method, headers, payload) => {
  try {
    const response = await fetch(url, {
      method: method,
      headers: headers,
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.log(error.message);
  }
};
