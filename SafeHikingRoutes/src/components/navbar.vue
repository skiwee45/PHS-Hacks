<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">
    <img src='data:image/png;base64,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' width="55" height="50" class="d-inline-block align-top" alt=".">
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="#">Safe Hiking Trails <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">About</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Contribute</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Contact</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Download
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
          <a class="dropdown-item" href="#">Dataset1</a>
          <a class="dropdown-item" href="#">Dataset2</a>
          <a class="dropdown-item" href="#">Dataset3</a>
        </div>
      </li>
    </ul>
  </div>
</nav>
</template>



