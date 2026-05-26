import { FileText, Upload, Edit, Save, X } from 'lucide-react';
import { useState } from 'react';
import { Resume } from './JobDetails';

interface ResumeManagerProps {
  resume: Resume | null;
  onSaveResume: (resume: Resume) => void;
}

export function ResumeManager({ resume, onSaveResume }: ResumeManagerProps) {
  const [isEditing, setIsEditing] = useState(!resume);
  const [formData, setFormData] = useState<Resume>(
    resume || {
      name: '',
      email: '',
      phone: '',
      skills: [],
      experience: [],
      education: []
    }
  );
  const [skillInput, setSkillInput] = useState('');
  const [experienceInput, setExperienceInput] = useState('');
  const [educationInput, setEducationInput] = useState('');

  const handleSave = () => {
    onSaveResume(formData);
    setIsEditing(false);
  };

  const handleAddSkill = () => {
    if (skillInput.trim()) {
      setFormData({
        ...formData,
        skills: [...formData.skills, skillInput.trim()]
      });
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (index: number) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter((_, idx) => idx !== index)
    });
  };

  const handleAddExperience = () => {
    if (experienceInput.trim()) {
      setFormData({
        ...formData,
        experience: [...formData.experience, experienceInput.trim()]
      });
      setExperienceInput('');
    }
  };

  const handleAddEducation = () => {
    if (educationInput.trim()) {
      setFormData({
        ...formData,
        education: [...formData.education, educationInput.trim()]
      });
      setEducationInput('');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-2">
          <FileText size={24} className="text-blue-600" />
          <h2 className="text-xl font-semibold">Your Resume</h2>
        </div>
        {resume && !isEditing && (
          <button
            onClick={() => setIsEditing(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Edit size={18} />
            Edit Resume
          </button>
        )}
      </div>

      {isEditing ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
              <input
                type="tel"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Skills</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                placeholder="Add a skill (e.g., JavaScript, Python)"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddSkill()}
              />
              <button
                onClick={handleAddSkill}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.skills.map((skill, idx) => (
                <span key={idx} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full flex items-center gap-1">
                  {skill}
                  <button onClick={() => handleRemoveSkill(idx)} className="hover:text-blue-900">
                    <X size={14} />
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Experience</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                placeholder="Add work experience (e.g., Software Engineer at ABC Corp, 2020-2023)"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={experienceInput}
                onChange={(e) => setExperienceInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddExperience()}
              />
              <button
                onClick={handleAddExperience}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add
              </button>
            </div>
            <ul className="space-y-2">
              {formData.experience.map((exp, idx) => (
                <li key={idx} className="text-gray-700 bg-gray-50 p-2 rounded">
                  {exp}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Education</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                placeholder="Add education (e.g., BS Computer Science, XYZ University, 2020)"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={educationInput}
                onChange={(e) => setEducationInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddEducation()}
              />
              <button
                onClick={handleAddEducation}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add
              </button>
            </div>
            <ul className="space-y-2">
              {formData.education.map((edu, idx) => (
                <li key={idx} className="text-gray-700 bg-gray-50 p-2 rounded">
                  {edu}
                </li>
              ))}
            </ul>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Save size={18} />
              Save Resume
            </button>
            {resume && (
              <button
                onClick={() => {
                  setIsEditing(false);
                  setFormData(resume);
                }}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
            )}
          </div>
        </div>
      ) : resume ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pb-4 border-b border-gray-200">
            <div>
              <p className="text-sm text-gray-600">Name</p>
              <p className="font-medium">{resume.name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Email</p>
              <p className="font-medium">{resume.email}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Phone</p>
              <p className="font-medium">{resume.phone}</p>
            </div>
          </div>

          <div>
            <h3 className="font-medium text-gray-700 mb-2">Skills</h3>
            <div className="flex flex-wrap gap-2">
              {resume.skills.map((skill, idx) => (
                <span key={idx} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-medium text-gray-700 mb-2">Experience</h3>
            <ul className="space-y-2">
              {resume.experience.map((exp, idx) => (
                <li key={idx} className="text-gray-700">• {exp}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-medium text-gray-700 mb-2">Education</h3>
            <ul className="space-y-2">
              {resume.education.map((edu, idx) => (
                <li key={idx} className="text-gray-700">• {edu}</li>
              ))}
            </ul>
          </div>
        </div>
      ) : null}
    </div>
  );
}
