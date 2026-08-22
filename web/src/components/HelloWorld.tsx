function Greeting({ name }: Readonly<{ name: string }>) {

  return <h1>Hello, {name}!</h1>;
}

export { Greeting };
