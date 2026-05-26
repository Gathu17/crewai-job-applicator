import { Job } from './JobCard';

export const mockJobs: Job[] = [
  {
    id: '1',
    title: 'Senior Frontend Developer',
    company: 'TechCorp Inc',
    location: 'San Francisco, CA',
    type: 'full-time',
    salary: '$120k - $160k',
    postedDate: '2 days ago',
    description: `We are looking for an experienced Frontend Developer to join our dynamic team. You will be responsible for building and maintaining our web applications using modern JavaScript frameworks.

The ideal candidate has a strong understanding of React, TypeScript, and modern web development practices. You will work closely with our design and backend teams to create exceptional user experiences.`,
    requirements: [
      '5+ years of experience in frontend development',
      'Strong proficiency in React and TypeScript',
      'Experience with state management (Redux, MobX, or similar)',
      'Knowledge of modern CSS frameworks and responsive design',
      'Strong problem-solving and communication skills',
      'Experience with Git and CI/CD pipelines'
    ]
  },
  {
    id: '2',
    title: 'Full Stack Engineer',
    company: 'StartupXYZ',
    location: 'New York, NY',
    type: 'full-time',
    salary: '$100k - $140k',
    postedDate: '5 days ago',
    description: `Join our innovative startup as a Full Stack Engineer! We're building the next generation of cloud-based productivity tools and need talented engineers who can work across the entire stack.

You'll have the opportunity to work with cutting-edge technologies and shape the direction of our product. We value creativity, collaboration, and a passion for building great software.`,
    requirements: [
      '3+ years of full stack development experience',
      'Proficiency in JavaScript/TypeScript and Node.js',
      'Experience with React or similar frontend frameworks',
      'Knowledge of SQL and NoSQL databases',
      'Familiarity with cloud platforms (AWS, Azure, or GCP)',
      'Agile/Scrum experience preferred'
    ]
  },
  {
    id: '3',
    title: 'Backend Developer',
    company: 'DataSystems Ltd',
    location: 'Austin, TX',
    type: 'full-time',
    salary: '$110k - $150k',
    postedDate: '1 week ago',
    description: `We're seeking a talented Backend Developer to help us build scalable, high-performance systems. You'll work on challenging problems involving large-scale data processing and API development.

Our tech stack includes Python, Node.js, PostgreSQL, and Redis. Experience with microservices architecture and containerization is a plus.`,
    requirements: [
      '4+ years of backend development experience',
      'Strong knowledge of Python or Node.js',
      'Experience with RESTful API design and development',
      'Proficiency in SQL databases',
      'Understanding of microservices architecture',
      'Experience with Docker and Kubernetes is a plus'
    ]
  },
  {
    id: '4',
    title: 'DevOps Engineer',
    company: 'CloudNative Co',
    location: 'Seattle, WA',
    type: 'full-time',
    salary: '$130k - $170k',
    postedDate: '3 days ago',
    description: `Looking for a DevOps Engineer to join our infrastructure team. You will be responsible for designing, implementing, and maintaining our cloud infrastructure and CI/CD pipelines.

We use AWS extensively and are looking for someone with strong experience in infrastructure as code, automation, and monitoring.`,
    requirements: [
      '5+ years of DevOps experience',
      'Strong AWS knowledge (EC2, S3, Lambda, etc.)',
      'Experience with Terraform or CloudFormation',
      'Proficiency in scripting (Python, Bash, or similar)',
      'Knowledge of Kubernetes and container orchestration',
      'Experience with monitoring tools (Prometheus, Grafana, etc.)'
    ]
  },
  {
    id: '5',
    title: 'UI/UX Designer',
    company: 'DesignFirst Agency',
    location: 'Los Angeles, CA',
    type: 'full-time',
    salary: '$90k - $120k',
    postedDate: '4 days ago',
    description: `We're looking for a creative UI/UX Designer to help us create beautiful and intuitive digital experiences. You'll work on a variety of projects across web and mobile platforms.

The ideal candidate has a strong portfolio demonstrating user-centered design thinking and excellent visual design skills.`,
    requirements: [
      '3+ years of UI/UX design experience',
      'Proficiency in Figma and Adobe Creative Suite',
      'Strong understanding of user-centered design principles',
      'Experience with prototyping and user testing',
      'Knowledge of HTML/CSS is a plus',
      'Excellent communication and collaboration skills'
    ]
  },
  {
    id: '6',
    title: 'Software Engineering Intern',
    company: 'BigTech Corp',
    location: 'Remote',
    type: 'internship',
    salary: '$30/hour',
    postedDate: '1 day ago',
    description: `Join our summer internship program and work on real projects that impact millions of users. You'll be paired with a mentor and have the opportunity to learn from experienced engineers.

We're looking for passionate students who are eager to learn and contribute to our codebase. This is a great opportunity to gain hands-on experience in a fast-paced environment.`,
    requirements: [
      'Currently pursuing a degree in Computer Science or related field',
      'Strong programming skills in at least one language',
      'Understanding of data structures and algorithms',
      'Good problem-solving abilities',
      'Team player with strong communication skills',
      'Available for 10-12 weeks during summer'
    ]
  }
];
